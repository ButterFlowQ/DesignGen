import React, { useState, useEffect, useRef } from "react";
import { JsonView, allExpanded, darkStyles } from "react-json-view-lite";
import plantumlEncoder from 'plantuml-encoder';
import { Maximize2, Minimize2, Download, ZoomIn, ZoomOut, RotateCcw } from 'lucide-react';
import type { ViewProps } from './types';

export const JavaLLD: React.FC<ViewProps> = ({ data }) => {
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [zoom, setZoom] = useState(100);
  const containerRef = useRef<HTMLDivElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);
  
  // If data is a string, assume it's PlantUML content
  const umlContent = typeof data === 'string' ? data : null;

  useEffect(() => {
    const calculateInitialZoom = () => {
      if (containerRef.current && imageRef.current) {
        const containerWidth = containerRef.current.clientWidth;
        const imageWidth = imageRef.current.naturalWidth;
        
        if (imageWidth > containerWidth) {
          // Calculate zoom to fit width with some padding
          const newZoom = Math.floor((containerWidth / imageWidth) * 100);
          setZoom(Math.min(Math.max(newZoom, 5), 100)); // Clamp between 5% and 100%
        } else {
          setZoom(100);
        }
      }
    };

    const image = imageRef.current;
    if (image) {
      if (image.complete) {
        calculateInitialZoom();
      } else {
        image.onload = calculateInitialZoom;
      }
    }

    return () => {
      if (image) {
        image.onload = null;
      }
    };
  }, [isFullscreen]);

  if (!umlContent) {
    return (
      <div className="doc-section">
        <h2>Java Low Level Design</h2>
        <JsonView data={data} shouldExpandNode={allExpanded} style={darkStyles} />
      </div>
    );
  }

  // Encode the PlantUML content
  const encodedUml = plantumlEncoder.encode(umlContent);
  const plantUmlUrl = `https://www.plantuml.com/plantuml/svg/${encodedUml}`;

  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = plantUmlUrl;
    link.download = 'uml-diagram.svg';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleZoomIn = () => {
    setZoom(prev => Math.min(prev + 10, 200));
  };

  const handleZoomOut = () => {
    setZoom(prev => Math.max(prev - 10, 5));
  };

  const handleZoomReset = () => {
    if (containerRef.current && imageRef.current) {
      const containerWidth = containerRef.current.clientWidth;
      const imageWidth = imageRef.current.naturalWidth;
      
      if (imageWidth > containerWidth) {
        // Calculate zoom to fit width with some padding
        const newZoom = Math.floor((containerWidth / imageWidth) * 100);
        setZoom(Math.min(Math.max(newZoom, 5), 100));
      } else {
        setZoom(100);
      }
    }
  };

  const handleZoomChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value, 10);
    if (!isNaN(value)) {
      setZoom(Math.max(5, Math.min(200, value)));
    }
  };

  return (
    <div className={`doc-section ${isFullscreen ? 'fixed inset-0 z-50 bg-white overflow-auto' : ''}`}>
      <div className="sticky top-0 bg-white z-10 pb-4">
        <div className="flex items-center justify-between">
          <h2>Java Low Level Design</h2>
          <div className="flex items-center gap-2">
            <div className="flex items-center bg-gray-100 rounded-lg p-1">
              <button
                onClick={handleZoomOut}
                className="p-2 hover:bg-white rounded transition-colors"
                title="Zoom out"
              >
                <ZoomOut className="h-4 w-4" />
              </button>
              <input
                type="number"
                value={zoom}
                onChange={handleZoomChange}
                className="w-16 px-2 text-sm text-center bg-transparent border-none focus:outline-none focus:ring-0"
                min="5"
                max="200"
                step="5"
              />
              <span className="text-sm text-gray-600 mr-1">%</span>
              <button
                onClick={handleZoomIn}
                className="p-2 hover:bg-white rounded transition-colors"
                title="Zoom in"
              >
                <ZoomIn className="h-4 w-4" />
              </button>
              <button
                onClick={handleZoomReset}
                className="p-2 hover:bg-white rounded transition-colors ml-1"
                title="Reset zoom"
              >
                <RotateCcw className="h-4 w-4" />
              </button>
            </div>
            <button
              onClick={handleDownload}
              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              title="Download SVG"
            >
              <Download className="h-5 w-5" />
            </button>
            <button
              onClick={() => setIsFullscreen(!isFullscreen)}
              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              title={isFullscreen ? "Exit fullscreen" : "Enter fullscreen"}
            >
              {isFullscreen ? (
                <Minimize2 className="h-5 w-5" />
              ) : (
                <Maximize2 className="h-5 w-5" />
              )}
            </button>
          </div>
        </div>
      </div>

      <div 
        ref={containerRef}
        className={`mt-4 bg-white rounded-lg shadow-sm ${isFullscreen ? 'p-8' : 'p-4'}`}
      >
        <div 
          className="overflow-auto"
          style={{
            maxHeight: isFullscreen ? 'calc(100vh - 12rem)' : '80vh',
            height: 'fit-content' // Add this to prevent extra space
          }}
        >
          <div
            style={{
              transform: `scale(${zoom / 100})`,
              transformOrigin: 'top left',
              width: 'fit-content',
              height: 'fit-content', // Add this to prevent extra space
              lineHeight: 0 // Add this to prevent extra space from line height
            }}
          >
            <img 
              ref={imageRef}
              src={plantUmlUrl} 
              alt="UML Diagram"
              className="max-w-none" // Prevent image from being constrained
              style={{
                display: 'block', // Remove default image spacing
                height: 'auto' // Ensure proper aspect ratio
              }}
              loading="lazy"
              onLoad={handleZoomReset}
            />
          </div>
        </div>
      </div>

      <div className="mt-4">
        <details className="bg-gray-50 rounded-lg">
          <summary className="px-4 py-2 cursor-pointer text-sm text-gray-600 hover:text-gray-900">
            View PlantUML Source
          </summary>
          <pre className="p-4 text-xs overflow-auto bg-gray-100 rounded-b-lg">
            <code>{umlContent}</code>
          </pre>
        </details>
      </div>
    </div>
  );
};