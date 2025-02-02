import React from "react";
import { JsonView, allExpanded, darkStyles } from "react-json-view-lite";
import {
  FunctionalRequirements,
  NonFunctionalRequirements,
  Architecture,
  ApiContracts,
  DatabaseSchema,
  JavaLLD,
} from "./DocumentTypeViews";

const DocumentRenderer = ({ document, html_document }) => {
  const parsedDoc = JSON.parse(document);
  const parsedHtmlDoc = JSON.parse(html_document);
  const documentComponents = {
    "functional requirements": FunctionalRequirements,
    "non functional requirements": NonFunctionalRequirements,
    architecture: Architecture,
    "api contracts": ApiContracts,
    "database schema": DatabaseSchema,
    "java LLD": JavaLLD,
  };
  //   console.log(parsedHtmlDoc);
  //   console.log(parsedHtmlDoc["java LLD"]);

  return (
    <div className="document-renderer">
      {parsedDoc &&
        Object.entries(parsedDoc).map(([key, value]) => {
          const Component = documentComponents[key];
          return Component ? (
            <Component key={key} data={value} html={parsedHtmlDoc[key]} />
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
