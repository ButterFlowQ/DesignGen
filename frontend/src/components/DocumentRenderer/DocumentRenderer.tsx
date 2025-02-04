import React from "react";
import ReactMarkdown from "react-markdown";
import { JsonView, allExpanded, darkStyles } from "react-json-view-lite";
import {
  FunctionalRequirements,
  NonFunctionalRequirements,
  Architecture,
  ApiContracts,
  DatabaseSchema,
  JavaLLD,
} from "./DocumentTypeViews";
import "react-json-view-lite/dist/index.css";
import "./DocumentRenderer.css";

interface DocumentRendererProps {
  document: string | null;
  htmlDocument: string | null;
}

export function DocumentRenderer({ document, htmlDocument }: DocumentRendererProps) {
  // Early return if no content is provided
  if (!document && !htmlDocument) {
    return (
      <div className="document-placeholder">
        <p>No document content available</p>
      </div>
    );
  }

  // Helper function to safely parse JSON with detailed validation
  const safeJsonParse = (jsonString: string | null, label = 'document') => {
    // Return empty object for null/undefined
    if (jsonString == null) {
      return {};
    }

    // Handle empty string
    if (jsonString.trim() === '') {
      return {};
    }

    try {
      const parsed = JSON.parse(jsonString);
      
      // Validate parsed result is an object
      if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) {
        return parsed;
      } else {
        console.warn(`Parsed ${label} is not an object:`, typeof parsed);
        return {};
      }
    } catch (error) {
      // Only log parsing errors for non-empty input
      if (jsonString.trim()) {
        console.warn(`Error parsing ${label}:`, error);
      }
      return {};
    }
  };

  // Parse documents with validation
  const parsedDoc = safeJsonParse(document);
  const parsedHtmlDoc = safeJsonParse(htmlDocument);

  const documentComponents = {
    "functional requirements": FunctionalRequirements,
    "non functional requirements": NonFunctionalRequirements,
    architecture: Architecture,
    "api contracts": ApiContracts,
    "database schema": DatabaseSchema,
    "java lld": JavaLLD,
  };

  // Check if we have valid JSON content
  const hasJsonContent = Object.keys(parsedDoc).length > 0 || Object.keys(parsedHtmlDoc).length > 0;

  // If we have no JSON content but have raw content, render it directly
  if (!hasJsonContent) {
    return (
      <div className="document-container">
        <div className="document-content">
          {document && typeof document === 'string' ? (
            <ReactMarkdown>{document}</ReactMarkdown>
          ) : htmlDocument && typeof htmlDocument === 'string' ? (
            <div dangerouslySetInnerHTML={{ __html: htmlDocument }} />
          ) : (
            <div className="document-placeholder">
              <p>No valid document content available</p>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Render structured content
  return (
    <div className="document-container">
      <div className="document-content">
        {Object.entries(parsedDoc).map(([key, value]) => {
          if (!key || value == null) return null;
          
          const Component = documentComponents[key.toLowerCase() as keyof typeof documentComponents];
          return Component ? (
            <Component 
              key={key} 
              data={value} 
              html={parsedHtmlDoc[key]}
            />
          ) : (
            <div key={key} className="json-fallback">
              <h2 className="text-xl font-bold mb-4 text-gray-800">
                {key}
              </h2>
              <JsonView
                data={value}
                shouldExpandNode={allExpanded}
                style={darkStyles}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
}