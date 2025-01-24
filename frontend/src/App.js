import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import DocumentView from "./DocumentView";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/doc/:documentId" element={<DocumentView />} />
      </Routes>
    </Router>
  );
}

export default App;
