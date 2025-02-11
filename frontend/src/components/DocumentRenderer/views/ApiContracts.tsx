import React from 'react';
import { SwaggerUIWrapper } from '../SwaggerUIWrapper';
import type { ViewProps } from './types';
import type { ApiSpec } from '@/types';

export const ApiContracts: React.FC<ViewProps> = ({ data }) => {
  const enhancedSpec: ApiSpec = {
    ...data,
    host:"localhost:8090",
    basePath: "",
    schemes: ["http"]
  };
  
  return (
    <div className="doc-section">
      <h2>API Contracts</h2>
      <div className="swagger-container">
        <SwaggerUIWrapper spec={enhancedSpec} />
      </div>
    </div>
  );
};