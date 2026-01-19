import type { ProjectModel } from "../types/product.types";

export default function ProjectItem({project}: {project: ProjectModel}){
    return (
        <div>
            <div>ID: {project.id}</div>
            <div>Name: {project.name}</div>
            <div>Key: {project.key}</div>
            <div>Access: {project.access}</div>
        </div>
    );
}