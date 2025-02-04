import React from 'react';
import type { ViewProps } from './types';
import type { DatabaseTable } from '@/types';

interface DatabaseSchemaProps extends ViewProps {
  data: {
    tables: DatabaseTable[];
  };
}

export const DatabaseSchema: React.FC<DatabaseSchemaProps> = ({ data }) => (
  <div className="doc-section">
    <h2>Database Schema</h2>
    {data.tables.map((table, tableIndex) => (
      <div key={tableIndex} className="schema-table">
        <h3>{table.name}</h3>
        <div className="table-container">
          <table>
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
                const foreignKey = table.foreignKeys?.find(
                  (fk) => fk.column === column.name
                );
                const indexes = table.indexes?.filter((idx) =>
                  idx.columns.includes(column.name)
                );

                return (
                  <tr key={columnIndex}>
                    <td>{column.name}</td>
                    <td>{`${column.type}${
                      column.length ? `(${column.length})` : ""
                    }${
                      column.precision
                        ? `(${column.precision},${column.scale})`
                        : ""
                    }`}</td>
                    <td>
                      {[
                        column.primaryKey && "PRIMARY KEY",
                        column.autoIncrement && "AUTO INCREMENT",
                        column.unique && "UNIQUE",
                        column.notNull && "NOT NULL",
                      ]
                        .filter(Boolean)
                        .join(", ")}
                    </td>
                    <td>
                      {foreignKey && (
                        <span className="foreign-key">
                          → {foreignKey.references.table}.
                          {foreignKey.references.column}
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
                          {index.unique && " (UNIQUE)"}
                        </div>
                      ))}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    ))}
  </div>
);