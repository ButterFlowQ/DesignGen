// Add or update these interfaces in your existing types file
export interface User {
  id: string;
  name: string;
  email: string;
  avatarUrl: string;
}

export interface Document {
  id: string;
  title: string;
  lastEdited: string;
}

export interface ChatMessage {
  id: number;
  message: string;
  from_id: string | null;
  to_id: string | null;
  is_user_message: boolean;
  creation_time: string;
}

export interface Message {
  text: string;
  sender: 'user' | 'bot';
  agent: string | null;
  timestamp: string;
}

export interface Agent {
  id: string;
  name: string;
  description?: string;
}

export interface ApiSpec {
  swagger: string;
  info: {
    title: string;
    version: string;
    description?: string;
  };
  host?: string;
  basePath?: string;
  schemes?: string[];
  paths: Record<string, any>;
  components?: {
    wrapComponents?: Record<string, any>;
    schemas?: Record<string, any>;
    securitySchemes?: Record<string, any>;
    parameters?: Record<string, any>;
    responses?: Record<string, any>;
    [key: string]: any;
  };
}

export interface DatabaseTable {
  name: string;
  columns: Array<{
    name: string;
    type: string;
    length?: number;
    precision?: number;
    scale?: number;
    primaryKey?: boolean;
    autoIncrement?: boolean;
    unique?: boolean;
    notNull?: boolean;
  }>;
  foreignKeys?: Array<{
    column: string;
    references: {
      table: string;
      column: string;
    };
    onDelete?: string;
    onUpdate?: string;
  }>;
  indexes?: Array<{
    name: string;
    columns: string[];
    unique?: boolean;
  }>;
}