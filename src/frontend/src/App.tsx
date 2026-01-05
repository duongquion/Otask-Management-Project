import { useEffect, useState } from "react";
type Project = {
  id: number;
  name: string;
};
function App() {
  const [projects, setProject] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc1MzMyMzQxLCJpYXQiOjE3Njc1NTYzNDEsImp0aSI6IjdiZWE4NjU4YzcxNDQxZjI5ODNlZDM4OTk2NmIxM2M1IiwidXNlcl9pZCI6ImE2MjBhYjRkLTg5ODUtNGJjYy05MmQ4LTRkYTFlNGVhNGJjNiJ9.YTo4qr6zZdAv-cmJHjQIoo0p4RP042zqmbphmiz33VQ");
    fetch("http://127.0.0.1:8000/project/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
    })
      .then(res => {
        if (!res.ok) throw new Error("API lỗi");
        return res.json();
      })
      .then(data => {
        setProject(data);
      })
      .catch(err => {
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <ul>
      {projects.map(p => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  );
}

export default App;
