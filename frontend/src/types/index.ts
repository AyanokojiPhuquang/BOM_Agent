export interface User {
  id: string;
  email: string;
  name: string;
  role: 'user' | 'admin';
}

export interface ImageAttachment {
  id: string;
  dataUrl: string;
  name: string;
  size: number;
}

export type MessageType = 'text' | 'tool_call' | 'tool_result';

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  type?: MessageType;
  toolName?: string;
  images?: ImageAttachment[];
  createdAt: number;
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: number;
  updatedAt: number;
}

export interface SSEToolCall {
  name: string;
  args?: Record<string, unknown>;
}

export interface SSEToolResult {
  name: string;
  content: string;
}

export interface SSEChunk {
  id: string;
  object: 'chat.completion.chunk';
  created: number;
  model: string;
  choices: {
    index: number;
    delta: {
      role?: string;
      content?: string;
      tool_call?: SSEToolCall;
      tool_result?: SSEToolResult;
    };
    finish_reason: string | null;
  }[];
}
