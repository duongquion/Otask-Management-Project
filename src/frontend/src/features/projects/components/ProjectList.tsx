import { useProject } from "../hooks/useProject";
import type { ProjectModel } from "../types/product.types";
import ProjectItem from "./ProjectItem";

export default function ProjectList(){
    const { projects, isLoading } = useProject();
    if (isLoading) return <div>Loading...</div>;
    
    return (
        <div>
            {projects.map((p: ProjectModel) => (
                <ProjectItem key={p.id} project={p} />
            ))}
        </div>
    );
}