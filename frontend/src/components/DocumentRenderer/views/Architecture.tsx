import React from 'react';
import type { ViewProps } from './types';

export const Architecture: React.FC<ViewProps> = ({ data }) => (
  <div className="doc-section">
    <h2>Architecture</h2>

    {data.high_level_overview && (
      <section className="arch-section">
        <h3>High Level Overview</h3>
        <p>{data.high_level_overview}</p>
      </section>
    )}

    {data.layers && data.layers.length > 0 && (
      <section className="arch-section">
        <h3>Layers</h3>
        {data.layers.map((layer: any, index: number) => (
          <div key={index} className="arch-subsection">
            <h4>{layer.layer_name}</h4>
            <p>{layer.description}</p>
            <h5>Primary Responsibilities:</h5>
            <ul>
              {layer.primary_responsibilities.map((resp: string, idx: number) => (
                <li key={idx}>{resp}</li>
              ))}
            </ul>
          </div>
        ))}
      </section>
    )}
  </div>
);