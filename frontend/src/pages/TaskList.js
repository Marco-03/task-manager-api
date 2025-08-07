import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");
  const [newStatus, setNewStatus] = useState("To do");
  const [editTaskId, setEditTaskId] = useState(null);
  const [editTitle, setEditTitle] = useState("");
  const [editStatus, setEditStatus] = useState("");
  const [filterStatus, setFilterStatus] = useState("All")
  const navigate = useNavigate();

  const fetchTasks = () => {
    const token = localStorage.getItem("token");

    fetch("http://localhost:5000/tasks", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Not authorized");
        return res.json();
      })
      .then((data) => setTasks(data))
      .catch(() => {
        localStorage.removeItem("token");
        navigate("/");
      });
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/");
      return;
    }

    fetchTasks();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  const handleCreateTask = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");

    const res = await fetch("http://localhost:5000/tasks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        title: newTask,
        status: newStatus,
      }),
    });

    if (res.ok) {
      fetchTasks();
      setNewTask("");
      setNewStatus("To do");
    }
  };

  const handleDeleteTask = async (id) => {
    const confirmDelete = window.confirm("Ești sigur că vrei să ștergi acest task?");
    if (!confirmDelete) return;

    const token = localStorage.getItem("token");

    const res = await fetch(`http://localhost:5000/tasks/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (res.ok) {
      fetchTasks();
    }
  };

  const handleEditClick = (task) => {
    setEditTaskId(task.id);
    setEditTitle(task.title);
    setEditStatus(task.status);
  };

  const handleCancelEdit = () => {
    setEditTaskId(null);
    setEditTitle("");
    setEditStatus("");
  };

  const handleSaveEdit = async () => {
    const token = localStorage.getItem("token");

    const res = await fetch(`http://localhost:5000/tasks/${editTaskId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        title: editTitle,
        status: editStatus,
      }),
    });

    if (res.ok) {
      fetchTasks();
      handleCancelEdit();
    }
  };

  const filteredTasks =
  filterStatus === "All"
    ? tasks
    : tasks.filter((task) => task.status === filterStatus);


  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow p-4 flex justify-between items-center sticky top-0 z-10">
        <h1 className="text-xl font-bold text-blue-600">Task Manager 📋</h1>
        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-4 py-1 rounded hover:bg-red-600"
        >
          Logout
        </button>
      </div>

      {/* Content */}

      <div className="p-6 max-w-2xl mx-auto">


  <div className="flex justify-between items-center mb-4">
  <h2 className="text-xl font-semibold">Filtrează după status:</h2>
  <select
    value={filterStatus}
    onChange={(e) => setFilterStatus(e.target.value)}
    className="p-2 border border-gray-300 rounded-xl"
  >
    <option value="All">Toate</option>
    <option value="To do">To do</option>
    <option value="In progress">In progress</option>
    <option value="Done">Done</option>
  </select>
</div>

        <form onSubmit={handleCreateTask} className="flex flex-col sm:flex-row gap-2 mb-6">
          <input
            type="text"
            placeholder="Titlul task-ului..."
            className="flex-grow border border-gray-300 p-3 rounded-xl focus:outline-blue-500"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
          />

          <select
            className="border border-gray-300 p-3 rounded-xl"
            value={newStatus}
            onChange={(e) => setNewStatus(e.target.value)}
          >
            <option value="To do">To do</option>
            <option value="In progress">In progress</option>
            <option value="Done">Done</option>
          </select>

          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded-xl hover:bg-blue-700 transition"
          >
            Adaugă
          </button>
        </form>

        <ul className="space-y-3">
          {filteredTasks.map((task) => {
            const statusColors = {
              "To do": "bg-gray-100 text-gray-700",
              "In progress": "bg-yellow-100 text-yellow-700",
              "Done": "bg-green-100 text-green-700",
            };

            const statusStyle = statusColors[task.status] || "bg-gray-100 text-gray-700";

            return (
              <li
                key={task.id}
                className={`p-4 rounded-xl shadow flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 transition hover:scale-[1.01] hover:shadow-md duration-200 ${statusStyle}`}
              >
                {editTaskId === task.id ? (
                  <div className="flex flex-col sm:flex-row gap-2 w-full">
                    <input
                      type="text"
                      className="flex-grow border border-gray-300 p-2 rounded-xl"
                      value={editTitle}
                      onChange={(e) => setEditTitle(e.target.value)}
                    />
                    <select
                      className="border border-gray-300 p-2 rounded-xl"
                      value={editStatus}
                      onChange={(e) => setEditStatus(e.target.value)}
                    >
                      <option value="To do">To do</option>
                      <option value="In progress">In progress</option>
                      <option value="Done">Done</option>
                    </select>
                  </div>
                ) : (
                  <div>
                    <p className="font-medium">{task.title}</p>
                    <p className="text-sm text-gray-600">{task.status}</p>
                  </div>
                )}

                <div className="flex gap-2">
                  {editTaskId === task.id ? (
                    <>
                      <button
                        onClick={handleSaveEdit}
                        className="bg-green-500 text-white px-3 py-1 rounded-xl text-sm"
                      >
                        Salvează
                      </button>
                      <button
                        onClick={handleCancelEdit}
                        className="bg-gray-300 px-3 py-1 rounded-xl text-sm"
                      >
                        Anulează
                      </button>
                    </>
                  ) : (
                    <>
                      <button
                        onClick={() => handleEditClick(task)}
                        className="bg-yellow-500 text-white px-3 py-1 rounded-xl text-sm"
                      >
                        Editează
                      </button>
                      <button
                        onClick={() => handleDeleteTask(task.id)}
                        className="bg-red-500 text-white px-3 py-1 rounded-xl text-sm"
                      >
                        🗑️
                      </button>
                    </>
                  )}
                </div>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );



}
