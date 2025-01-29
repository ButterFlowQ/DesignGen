import React from "react";
import { JsonView, allExpanded, darkStyles } from "react-json-view-lite";
import '../styles/DatabaseSchema.css';
import '../styles/ApiContracts.css';

export const FunctionalRequirements = ({ data, html }) => (
  <div className="doc-section">
    <h2>Functional Requirements</h2>
    <ul>
      {data.map((req, index) => (
        <li key={index}>{req}</li>
      ))}
    </ul>
  </div>
);

export const NonFunctionalRequirements = ({ data, html }) => (
  <div className="doc-section">
    <h2>Non-Functional Requirements</h2>
    <ul>
      {data.map((req, index) => (
        <li key={index}>{req}</li>
      ))}
    </ul>
  </div>
);

export const Architecture = ({ data, html }) => (
  <div className="doc-section">
    <h2>Architecture</h2>
    <div style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
      {data}
    </div>
  </div>
);

export const ApiContracts = ({ data, html }) => (
  <div className="doc-section">
    <h2>API Contracts</h2>
    <div className="api-info">
      <h3>{data.info.title} - v{data.info.version}</h3>
    </div>
    <table className="api-table">
      <thead>
        <tr>
          <th>Method</th>
          <th>Path</th>
          <th>Description</th>
          <th>Parameters</th>
          <th>Response</th>
        </tr>
      </thead>
      <tbody>
        {Object.entries(data.paths).map(([path, methods]) =>
          Object.entries(methods).map(([method, details]) => (
            <tr key={`${path}-${method}`}>
              <td>
                <span className={`method-type method-${method.toLowerCase()}`}>
                  {method.toUpperCase()}
                </span>
              </td>
              <td className="path-cell">
                <code>{path}</code>
              </td>
              <td>{details.summary}</td>
              <td>
                {details.parameters && details.parameters.length > 0 ? (
                  <table className="nested-table">
                    <tbody>
                      {details.parameters.map((param, index) => (
                        <tr key={index}>
                          <td>
                            <code>{param.name}</code>
                            <small className="param-in">({param.in})</small>
                            <br />
                            <small className="param-type">
                              {param.type}
                              {param.required && ' - required'}
                            </small>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <small>No parameters</small>
                )}
              </td>
              <td>
                <table className="nested-table">
                  <tbody>
                    {Object.entries(details.responses).map(([code, response]) => (
                      <tr key={code}>
                        <td>
                          <span className={`response-code code-${code.charAt(0)}xx`}>
                            {code}
                          </span>
                          <br />
                          <small>{response.description}</small>
                          {response.schema && (
                            <div className="schema-preview">
                              {Object.entries(response.schema.properties || {}).map(([prop, schema]) => (
                                <div key={prop} className="schema-prop">
                                  <code>{prop}</code>: {schema.type}
                                </div>
                              ))}
                            </div>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </td>
            </tr>
          ))
        )}
      </tbody>
    </table>
  </div>
);

export const DatabaseSchema = ({ data, html }) => (
  <div className="doc-section">
    <h2>Database Schema</h2>
    {data.tables.map((table, tableIndex) => (
      <div key={tableIndex} className="schema-table">
        <h3>{table.name}</h3>
        <table className="table">
          <thead>
            <tr>
              <th>Column Name</th>
              <th>Type</th>
              <th>Constraints</th>
              <th>Foreign Key</th>
              <th>Indexes</th>
            </tr>
          </thead>
          <tbody>
            {table.columns.map((column, columnIndex) => {
              const foreignKey = table.foreignKeys?.find(fk => fk.column === column.name);
              const indexes = table.indexes?.filter(idx => idx.columns.includes(column.name));
              
              return (
                <tr key={columnIndex}>
                  <td>{column.name}</td>
                  <td>{`${column.type}${column.length ? `(${column.length})` : ''}${
                    column.precision ? `(${column.precision},${column.scale})` : ''
                  }`}</td>
                  <td>
                    {[
                      column.primaryKey && 'PRIMARY KEY',
                      column.autoIncrement && 'AUTO INCREMENT',
                      column.unique && 'UNIQUE',
                      column.notNull && 'NOT NULL',
                    ]
                      .filter(Boolean)
                      .join(', ')}
                  </td>
                  <td>
                    {foreignKey && (
                      <span className="foreign-key">
                        → {foreignKey.references.table}.{foreignKey.references.column}
                        <br />
                        <small>
                          ON DELETE {foreignKey.onDelete}
                          <br />
                          ON UPDATE {foreignKey.onUpdate}
                        </small>
                      </span>
                    )}
                  </td>
                  <td>
                    {indexes?.map((index, idx) => (
                      <div key={idx} className="index-entry">
                        {index.name}
                        {index.unique && ' (UNIQUE)'}
                      </div>
                    ))}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    ))}
  </div>
);

export const JavaLLD = ({ data, html }) => (
  <div className="doc-section">
    <h2>Java Low Level Design</h2>
    {html ? (
      <div 
        dangerouslySetInnerHTML={{ __html: html }} 
        style={{ 
          transform: 'scale(0.5)', 
          transformOrigin: 'top left',
          marginBottom: '-50%' // Compensate for the scaling
        }}
      />
    ) : (
        <JsonView
            data={data}
            shouldExpandNode={allExpanded}
            style={darkStyles}
        />
    )}
  </div>
);