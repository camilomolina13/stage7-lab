import { Link, Route, Routes } from "react-router-dom";
import ProjectTasksPage from "./pages/ProjectTasksPage";
import ProjectsPage from "./pages/ProjectsPage";

export default function App() {
  return (
    <>
      <header className="topbar">
        <Link to="/">PROJECT TRACKER</Link>
      </header>
      <main className="container">
        <Routes>
          <Route path="/" element={<ProjectsPage />} />
          <Route path="/projects/:projectId" element={<ProjectTasksPage />} />
          <Route path="*" element={<p>Page not found. <Link to="/">Back to projects</Link></p>} />
        </Routes>
      </main>
    </>
  );
}