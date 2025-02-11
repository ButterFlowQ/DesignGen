import React from 'react';
import SwaggerUI from 'swagger-ui-react';
import type { ApiSpec } from '@/types';

interface SwaggerErrorBoundaryProps {
  children: React.ReactNode;
}

interface SwaggerErrorBoundaryState {
  hasError: boolean;
}

// Error boundary for SwaggerUI
class SwaggerErrorBoundary extends React.Component<SwaggerErrorBoundaryProps, SwaggerErrorBoundaryState> {
  constructor(props: SwaggerErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): SwaggerErrorBoundaryState {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    console.debug('SwaggerUI encountered an error:', error);
  }

  render(): React.ReactNode {
    if (this.state.hasError) {
      return (
        <div className="p-4 text-red-600">
          Error loading API documentation. Please try refreshing the page.
        </div>
      );
    }

    return this.props.children;
  }
}

interface ModernSchemesProps {
  schemes?: string[];
  children: React.ReactNode;
}

interface ModernSchemesState {
  schemes: string[];
}

// Modern class components to replace the legacy ones
class ModernSchemes extends React.Component<ModernSchemesProps, ModernSchemesState> {
  state: ModernSchemesState = {
    schemes: this.props.schemes || []
  };

  static getDerivedStateFromProps(props: ModernSchemesProps, state: ModernSchemesState): Partial<ModernSchemesState> | null {
    if (props.schemes !== state.schemes) {
      return { schemes: props.schemes || [] };
    }
    return null;
  }

  render(): React.ReactNode {
    return <div className="schemes-wrapper">{this.props.children}</div>;
  }
}

interface ModernOperationContainerProps {
  operation: Record<string, any>;
  children: React.ReactNode;
}

interface ModernOperationContainerState {
  operation: Record<string, any>;
}

class ModernOperationContainer extends React.Component<ModernOperationContainerProps, ModernOperationContainerState> {
  state: ModernOperationContainerState = {
    operation: this.props.operation
  };

  static getDerivedStateFromProps(
    props: ModernOperationContainerProps, 
    state: ModernOperationContainerState
  ): Partial<ModernOperationContainerState> | null {
    if (props.operation !== state.operation) {
      return { operation: props.operation };
    }
    return null;
  }

  render(): React.ReactNode {
    return <div className="operation-container">{this.props.children}</div>;
  }
}

interface SwaggerUIWrapperProps {
  spec: ApiSpec;
  [key: string]: any;
}

// Wrapper component using modern React patterns
export const SwaggerUIWrapper = React.memo(function SwaggerUIWrapper({ spec, ...props }: SwaggerUIWrapperProps) {
  // Memoize the enhanced spec
  const enhancedSpec = React.useMemo(() => ({
    ...spec,
    components: {
      ...spec.components,
      wrapComponents: {
        Schemes: () => ModernSchemes,
        OperationContainer: () => ModernOperationContainer
      }
    }
  }), [spec]);

  return (
    <SwaggerErrorBoundary>
      <div className="swagger-ui-wrapper">
        <SwaggerUI 
          spec={enhancedSpec} 
          {...props}
          defaultModelsExpandDepth={-1}
          docExpansion="list"
        />
      </div>
    </SwaggerErrorBoundary>
  );
});

SwaggerUIWrapper.displayName = 'SwaggerUIWrapper';