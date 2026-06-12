# Requirements Document

## Introduction

This feature integrates Google Drive with OAuth 2.0 authorization to allow authenticated users to connect their Google Drive account, select a folder, and automatically import all PDF files from that folder into the existing product extraction pipeline (pdfplumber → LLM → Products DB). Processing is handled asynchronously via a Redis-backed message queue with real-time progress updates delivered to the frontend over WebSockets.

## Glossary

- **OAuth_Service**: The backend service responsible for initiating and completing the Google OAuth 2.0 authorization flow, including consent URL generation and token exchange.
- **Token_Manager**: The backend component that stores, retrieves, and refreshes Google OAuth 2.0 tokens (access_token and refresh_token) in PostgreSQL.
- **Folder_Scanner**: The backend service that recursively enumerates all PDF files within a user-specified Google Drive folder using the Google Drive API.
- **Sync_Orchestrator**: The backend service that coordinates a batch sync job — creating tasks for each discovered PDF, dispatching them to the message queue, and tracking overall batch progress.
- **Task_Worker**: A background worker process that consumes PDF processing tasks from Redis, downloads the file from Google Drive, and invokes the existing extraction pipeline.
- **Extraction_Pipeline**: The existing pipeline (pdfplumber text extraction → LLM structured extraction → save to Products table) located in `backend/src/services/pdf_converter.py`.
- **Progress_Notifier**: The WebSocket-based subsystem that pushes real-time job progress events to connected frontend clients.
- **Dead_Letter_Queue**: A secondary Redis queue that stores tasks which have failed after all retry attempts, for later inspection or manual reprocessing.
- **Drive_Picker**: A frontend UI component (Google Picker API or manual Folder ID input) that allows users to select a Google Drive folder.
- **Sync_Dashboard**: The frontend UI that displays active and historical sync jobs with per-file progress indicators.

## Requirements

### Requirement 1: OAuth 2.0 Authorization Initiation

**User Story:** As a user, I want to click a "Sign in with Google" button so that I can authorize the system to read my Google Drive files.

#### Acceptance Criteria

1. WHEN the user requests Google authorization, THE OAuth_Service SHALL generate a Google OAuth 2.0 consent URL with `drive.readonly` scope and `access_type=offline`.
2. WHEN generating the consent URL, THE OAuth_Service SHALL include a CSRF state parameter bound to the user's session.
3. WHEN the consent URL is generated, THE OAuth_Service SHALL return the URL to the frontend for redirect.
4. THE OAuth_Service SHALL read Google OAuth client credentials (client_id, client_secret, redirect_uri) from environment variables defined in the project root `.env` file.

### Requirement 2: OAuth 2.0 Callback and Token Exchange

**User Story:** As a user, I want the system to securely complete the OAuth handshake after I grant consent so that my authorization is persisted.

#### Acceptance Criteria

1. WHEN Google redirects to the callback endpoint with an authorization code, THE OAuth_Service SHALL exchange the code for an access_token and refresh_token using Google's token endpoint.
2. WHEN the callback is received, THE OAuth_Service SHALL validate the CSRF state parameter against the user's session before processing.
3. IF the state parameter is invalid or missing, THEN THE OAuth_Service SHALL reject the request with a 403 Forbidden response.
4. IF the token exchange fails, THEN THE OAuth_Service SHALL return an error response with a descriptive message and log the failure.
5. WHEN tokens are successfully obtained, THE OAuth_Service SHALL pass them to the Token_Manager for persistence.

### Requirement 3: Token Persistence and Refresh

**User Story:** As a user, I want my Google authorization to persist across sessions so that I do not need to re-authorize every time I use the sync feature.

#### Acceptance Criteria

1. WHEN tokens are received from the OAuth flow, THE Token_Manager SHALL store the access_token, refresh_token, token expiry timestamp, and associated user_id in PostgreSQL.
2. THE Token_Manager SHALL encrypt the refresh_token at rest before storing it in the database.
3. WHEN a Google API call requires authentication, THE Token_Manager SHALL check the access_token expiry and return a valid token.
4. IF the access_token is expired, THEN THE Token_Manager SHALL use the refresh_token to obtain a new access_token from Google's token endpoint and update the stored record.
5. IF the refresh_token is revoked or invalid, THEN THE Token_Manager SHALL mark the user's Google connection as disconnected and notify the frontend.

### Requirement 4: Google Drive Folder Selection

**User Story:** As a user, I want to select a Google Drive folder so that the system knows which folder to scan for PDF files.

#### Acceptance Criteria

1. THE Sync_Dashboard SHALL provide a UI mechanism for the user to specify a Google Drive folder (via folder ID input or the Google Picker API).
2. WHEN a folder is selected, THE Folder_Scanner SHALL validate that the folder exists and is accessible with the user's stored credentials.
3. IF the folder is inaccessible or does not exist, THEN THE Folder_Scanner SHALL return an error message indicating the folder cannot be accessed.
4. WHEN the folder is validated, THE Sync_Orchestrator SHALL store the selected folder ID associated with the user for future sync operations.

### Requirement 5: Recursive PDF Discovery

**User Story:** As a user, I want the system to find all PDF files in my selected folder and its subfolders so that nothing is missed.

#### Acceptance Criteria

1. WHEN a sync job is initiated, THE Folder_Scanner SHALL recursively enumerate all files with MIME type `application/pdf` within the selected folder and all nested subfolders.
2. THE Folder_Scanner SHALL use paginated Google Drive API requests to handle folders containing more than 100 files.
3. THE Folder_Scanner SHALL return a list of discovered PDF files including file ID, file name, and file size for each entry.
4. IF the Google Drive API returns a rate-limit error, THEN THE Folder_Scanner SHALL apply exponential backoff and retry the request up to 5 times.
5. WHILE scanning is in progress, THE Folder_Scanner SHALL report the number of files discovered so far to the Sync_Orchestrator.

### Requirement 6: Batch Job Creation and Queue Dispatch

**User Story:** As a user, I want the system to queue all discovered PDFs for background processing so that the operation does not block the UI.

#### Acceptance Criteria

1. WHEN the Folder_Scanner completes discovery, THE Sync_Orchestrator SHALL create a batch job record in PostgreSQL with status "processing", total file count, and timestamp.
2. THE Sync_Orchestrator SHALL enqueue one task per discovered PDF file into the Redis message queue with the file's Google Drive ID, file name, batch job ID, and user ID.
3. THE Sync_Orchestrator SHALL assign a unique task ID to each enqueued task for individual tracking.
4. IF the Redis queue is unavailable, THEN THE Sync_Orchestrator SHALL mark the batch job as "failed" and return an error to the user.

### Requirement 7: Background PDF Processing

**User Story:** As a user, I want each PDF to be downloaded and processed through the existing extraction pipeline so that product data is extracted automatically.

#### Acceptance Criteria

1. WHEN the Task_Worker picks up a task from the Redis queue, THE Task_Worker SHALL download the PDF file from Google Drive using the user's stored access_token.
2. WHEN the PDF is downloaded, THE Task_Worker SHALL invoke the Extraction_Pipeline (pdfplumber text extraction followed by LLM structured product spec extraction).
3. WHEN the Extraction_Pipeline returns product specs, THE Task_Worker SHALL save each extracted product to the Products table in PostgreSQL with a reference to the source Google Drive file.
4. WHEN processing completes successfully, THE Task_Worker SHALL update the task status to "completed" and notify the Progress_Notifier.
5. IF the PDF download fails due to an expired token, THEN THE Task_Worker SHALL request a refreshed token from the Token_Manager and retry the download once.

### Requirement 8: Retry and Dead Letter Queue

**User Story:** As a user, I want failed PDF tasks to be retried automatically and permanently failed tasks to be stored for review so that no data is silently lost.

#### Acceptance Criteria

1. IF a task fails during processing, THEN THE Task_Worker SHALL retry the task up to 3 times with exponential backoff.
2. IF a task fails after all retry attempts, THEN THE Task_Worker SHALL move the task to the Dead_Letter_Queue with the original payload and the error details.
3. THE Dead_Letter_Queue SHALL retain failed tasks for a minimum of 7 days.
4. THE Sync_Dashboard SHALL display tasks in the Dead_Letter_Queue with their error messages and allow manual retry.

### Requirement 9: Real-Time Progress Updates

**User Story:** As a user, I want to see real-time progress of my sync job so that I know how many files have been processed.

#### Acceptance Criteria

1. WHEN a task status changes (queued, processing, completed, failed), THE Progress_Notifier SHALL emit a WebSocket event to the user's connected frontend session.
2. THE Progress_Notifier SHALL include the batch job ID, task ID, current status, and overall batch progress (completed count / total count) in each event.
3. WHILE a batch job is in progress, THE Sync_Dashboard SHALL display a progress bar showing the percentage of completed tasks.
4. WHEN all tasks in a batch are completed or moved to the Dead_Letter_Queue, THE Progress_Notifier SHALL emit a batch-complete event with a summary (success count, failure count).

### Requirement 10: Progress Bar UI

**User Story:** As a user, I want a visual progress bar in the UI showing the status of my batch sync job so that I can monitor it at a glance.

#### Acceptance Criteria

1. THE Sync_Dashboard SHALL display the batch job status with a progress bar indicating (completed + failed) / total tasks.
2. THE Sync_Dashboard SHALL show individual file status indicators (queued, processing, completed, failed) for each PDF in the batch.
3. WHEN a batch job completes, THE Sync_Dashboard SHALL display a summary showing total files processed, products extracted, and failures.
4. THE Sync_Dashboard SHALL allow users to view historical sync jobs with their completion status and extracted product counts.

### Requirement 11: Environment Configuration

**User Story:** As a developer, I want all sensitive configuration (Google OAuth secrets, Redis URL) stored in the project root `.env` file so that deployment is straightforward and consistent.

#### Acceptance Criteria

1. THE OAuth_Service SHALL read `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `GOOGLE_REDIRECT_URI` from environment variables.
2. THE Task_Worker SHALL read the Redis connection URL from the `REDIS_URL` environment variable.
3. THE Token_Manager SHALL read the token encryption key from the `TOKEN_ENCRYPTION_KEY` environment variable.
4. THE system SHALL provide a `.env.example` file at the project root documenting all new environment variables required for the Google Drive Sync feature.
5. THE Docker Compose configuration SHALL include a Redis service accessible to the backend and worker services.

### Requirement 12: Duplicate Detection

**User Story:** As a user, I want the system to skip files that have already been processed so that I do not get duplicate products in the database.

#### Acceptance Criteria

1. WHEN enqueueing tasks, THE Sync_Orchestrator SHALL check if a file (by Google Drive file ID) has already been successfully processed in a previous batch.
2. IF a file has already been processed, THEN THE Sync_Orchestrator SHALL skip that file and exclude it from the batch count.
3. THE Sync_Dashboard SHALL indicate how many files were skipped due to prior processing.

### Requirement 13: Google Account Disconnection

**User Story:** As a user, I want to disconnect my Google account from the system so that my tokens are removed and access is revoked.

#### Acceptance Criteria

1. WHEN the user requests disconnection, THE Token_Manager SHALL delete all stored tokens for that user from the database.
2. WHEN disconnection is requested, THE OAuth_Service SHALL attempt to revoke the token with Google's revocation endpoint.
3. IF the revocation request fails, THEN THE OAuth_Service SHALL still delete local tokens and log the revocation failure.
4. WHEN the account is disconnected, THE Sync_Dashboard SHALL update the UI to show the disconnected state and display the "Sign in with Google" button.
