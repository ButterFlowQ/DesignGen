// Add these interfaces to your existing types file
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
  createdBy: string;
}

// Rest of your existing types...