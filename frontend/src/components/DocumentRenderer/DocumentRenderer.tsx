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
  document: Record<string, any> | null;
  htmlDocument: Record<string, any> | null;
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

  const documentComponents = {
    "functional requirements": FunctionalRequirements,
    "non functional requirements": NonFunctionalRequirements,
    architecture: Architecture,
    "api contracts": ApiContracts,
    "database schema": DatabaseSchema,
    "java lld": JavaLLD,
  };

  // Render structured content
  return (
    <div className="document-container">
      <div className="document-content">
        {document && Object.entries(document).map(([key, value]) => {
          if (!key || value == null) return null;
          
          const Component = documentComponents[key.toLowerCase() as keyof typeof documentComponents];
          return Component ? (
            <Component 
              key={key} 
              data={value} 
              html={htmlDocument?.[key]}
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