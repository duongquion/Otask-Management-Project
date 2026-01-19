import { useEffect, useState } from "react";
import type { ProjectModel } from "../types/product.types";
import { getProject } from "../services/project.service";

export const useProject = () =>{
    const [projects, setProject] = useState<ProjectModel[]>([]);
    const [isLoading, setLoading] = useState(true);

    useEffect(() => {
        getProject().then((data) => {
            setProject(data),
            setLoading(false)
        })
    }, [])

    return { projects, isLoading };
}