// ---------------------------------------------------------------------------
// Application-wide constants
// ---------------------------------------------------------------------------

export const APP_NAME = 'Starlink Chat';
export const AI_NAME = 'Starlink AI';
export const AI_DISCLAIMER =
  'Starlink AI may produce inaccurate information. Verify important facts.';
export const WELCOME_HEADING = 'Welcome to Starlink Chat';

export const Z_INDEX = {
  SIDEBAR_OVERLAY: 20,
  SIDEBAR: 30,
  MODAL: 50,
} as const;

export const TEXTAREA_MAX_HEIGHT = 200;
export const COPY_FEEDBACK_MS = 2000;

/** Shared input class used across modal forms */
export const INPUT_CLASS =
  'w-full px-3 py-2 rounded-lg bg-dark-bg border border-dark-border text-white text-sm focus:outline-none focus:border-accent';
