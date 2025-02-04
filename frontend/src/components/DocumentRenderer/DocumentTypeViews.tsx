import React from "react";
import { JsonView, allExpanded, darkStyles } from "react-json-view-lite";
import {
  FunctionalRequirements,
  NonFunctionalRequirements,
  Architecture,
  ApiContracts,
  DatabaseSchema,
  JavaLLD
} from './views';
import type { DatabaseTable, ApiSpec } from '@/types';
import "swagger-ui-react/swagger-ui.css";
import "./styles/DatabaseSchema.css";
import "./styles/ApiContracts.css";
import "./styles/Architecture.css";

export {
  FunctionalRequirements,
  NonFunctionalRequirements,
  Architecture,
  ApiContracts,
  DatabaseSchema,
  JavaLLD
};