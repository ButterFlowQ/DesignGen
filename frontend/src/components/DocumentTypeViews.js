import React from "react";
import { JsonView, allExpanded, darkStyles } from "react-json-view-lite";
import "../styles/DatabaseSchema.css";
import "../styles/ApiContracts.css";
import "../styles/Architecture.css";
import SwaggerUI from "swagger-ui-react";
import "swagger-ui-react/swagger-ui.css";

export const FunctionalRequirements = ({ data, html }) => (
  <div className="doc-section">
    <h2>Functional Requirements</h2>
    <ul>
      {data.map((req, index) => (
        <li key={index}>
          <JsonView data={req}></JsonView>
        </li>
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

    {/* High Level Overview */}
    <section className="arch-section">
      <h3>High Level Overview</h3>
      <p>{data.high_level_overview}</p>
    </section>

    {/* Layers */}
    <section className="arch-section">
      <h3>Layers</h3>
      {data.layers.map((layer, index) => (
        <div key={index} className="arch-subsection">
          <h4>{layer.layer_name}</h4>
          <p>{layer.description}</p>
          <h5>Primary Responsibilities:</h5>
          <ul>
            {layer.primary_responsibilities.map((resp, idx) => (
              <li key={idx}>{resp}</li>
            ))}
          </ul>
        </div>
      ))}
    </section>

    {/* Services */}
    <section className="arch-section">
      <h3>Services</h3>
      {data.services.map((service, index) => (
        <div key={index} className="arch-subsection">
          <h4>{service.name}</h4>
          <h5>Purpose/Responsibilities:</h5>
          <ul>
            {service.purpose_or_responsibilities.map((resp, idx) => (
              <li key={idx}>{resp}</li>
            ))}
          </ul>
          <h5>Dependencies:</h5>
          <ul>
            {service.dependencies.map((dep, idx) => (
              <li key={idx}>{dep}</li>
            ))}
          </ul>
          <p>
            <strong>Scalability Strategy:</strong>{" "}
            {service.scalability_strategy}
          </p>
          <h5>Fault Tolerance Mechanisms:</h5>
          <ul>
            {service.fault_tolerance_mechanisms.map((mech, idx) => (
              <li key={idx}>{mech}</li>
            ))}
          </ul>
        </div>
      ))}
    </section>

    {/* Data Flow */}
    <section className="arch-section">
      <h3>Data Flow</h3>
      {data.data_flow.map((flow, index) => (
        <div key={index} className="arch-subsection">
          <h4>{flow.name}</h4>
          <h5>Steps:</h5>
          <ol>
            {flow.steps.map((step, idx) => (
              <li key={idx}>{step}</li>
            ))}
          </ol>
          <h5>Critical Paths:</h5>
          <ul>
            {flow.critical_paths.map((path, idx) => (
              <li key={idx}>{path}</li>
            ))}
          </ul>
        </div>
      ))}
    </section>

    {/* Cross-cutting Concerns */}
    <section className="arch-section">
      <h3>Cross-cutting Concerns</h3>
      <div className="arch-subsection">
        <h4>Security and Compliance</h4>
        <p>
          <strong>Authentication/Authorization:</strong>{" "}
          {
            data.cross_cutting_concerns.security_and_compliance
              .authentication_authorization
          }
        </p>
        <p>
          <strong>Data Protection:</strong>{" "}
          {data.cross_cutting_concerns.security_and_compliance.data_protection}
        </p>
        <p>
          <strong>Compliance Standards:</strong>{" "}
          {
            data.cross_cutting_concerns.security_and_compliance
              .compliance_standards
          }
        </p>
      </div>
      <div className="arch-subsection">
        <h4>Observability</h4>
        <p>
          <strong>Logging:</strong>{" "}
          {data.cross_cutting_concerns.observability.logging}
        </p>
        <p>
          <strong>Monitoring:</strong>{" "}
          {data.cross_cutting_concerns.observability.monitoring}
        </p>
        <p>
          <strong>Alerting:</strong>{" "}
          {data.cross_cutting_concerns.observability.alerting}
        </p>
      </div>
    </section>

    {/* Trade-offs and Rationale */}
    <section className="arch-section">
      <h3>Trade-offs and Rationale</h3>
      {data.trade_offs_and_rationale.map((item, index) => (
        <div key={index} className="arch-subsection">
          <h4>{item.decision}</h4>
          <p>{item.rationale}</p>
        </div>
      ))}
    </section>
  </div>
);

export const ApiContracts = ({ data, html }) => {
  data.host = "localhost:8090";
  data.basePath = "";
  data.schemes = ["http"];
  return (
    <div className="doc-section">
      <h2>API Contracts</h2>
      <SwaggerUI spec={data} />
    </div>
  );
};

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
          transform: "scale(0.5)",
          transformOrigin: "top left",
          marginBottom: "-50%", // Compensate for the scaling
        }}
      />
    ) : (
      <JsonView data={data} shouldExpandNode={allExpanded} style={darkStyles} />
    )}
  </div>
);
