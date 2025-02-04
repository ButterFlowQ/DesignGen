import React from 'react';
import type { ViewProps } from './types';

export const FunctionalRequirements: React.FC<ViewProps> = ({ data }) => (
  <div className="doc-section">
    <h2>Functional Requirements</h2>
    <ul className="requirements-list">
      {data.map((req: string, index: number) => (
        <li key={index} className="requirement-item">{req}</li>
      ))}
    </ul>
  </div>
);