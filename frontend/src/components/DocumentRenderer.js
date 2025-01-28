import React from "react";
import {
  JsonView,
  allExpanded,
  darkStyles,
} from "react-json-view-lite";
import {
  FunctionalRequirements,
  NonFunctionalRequirements,
  Architecture,
  ApiContracts,
  DatabaseSchema,
  JavaLLD,
} from "./DocumentTypeViews";

const DocumentRenderer = ({ document }) => {
  const parsedDoc = JSON.parse(document);
  const documentComponents = {
    "functional requirements": FunctionalRequirements,
    "non functional requirements": NonFunctionalRequirements,
    "architecture": Architecture,
    "api contracts": ApiContracts,
    "database schema": DatabaseSchema,
    "java LLD": JavaLLD,
  };

  return (
    <div className="document-renderer">
      {Object.entries(parsedDoc).map(([key, value]) => {
        const Component = documentComponents[key.toLowerCase()];
        return Component ? (
          <Component key={key} data={value} />
        ) : (
          <JsonView
            key={key}
            data={{ [key]: value }}
            shouldExpandNode={allExpanded}
            style={darkStyles}
          />
        );
      })}
    </div>
  );
};

export default DocumentRenderer; 