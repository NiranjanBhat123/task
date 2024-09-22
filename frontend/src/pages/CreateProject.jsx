import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { createProject, getUsers } from '../services/api';
import { TextField, MenuItem, Checkbox, ListItemText, Button, CircularProgress } from '@mui/material';
import { Select, FormControl, InputLabel } from '@mui/material';

function CreateProject() {
  const [projectData, setProjectData] = useState({
    name: '',
    description: '',
    contributors: [],
    taskTitle: '',
    taskDescription: '',
    taskAssignedTo: '',
  });
  const [users, setUsers] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await getUsers();
      setUsers(response);
    } catch (err) {
      setError('Error fetching users');
    }
  };

  const handleChange = (e) => {
    setProjectData({ ...projectData, [e.target.name]: e.target.value });
  };

  const handleContributorsChange = (event) => {
    setProjectData({ ...projectData, contributors: event.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const formattedData = {
        name: projectData.name,
        description: projectData.description,
        contributors: projectData.contributors,
        tasks: [
          {
            title: projectData.taskTitle,
            description: projectData.taskDescription,
            assigned_to: projectData.taskAssignedTo,
          },
        ],
      };

      const response = await createProject(formattedData);
      setSuccess('Project created successfully!');
      setTimeout(() => {
        navigate(`/projects/${response.id}`);
      }, 1500);
    } catch (err) {
      setError('Error creating project. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">Create New Project</h2>
      {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">{error}</div>}
      {success && <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">{success}</div>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <TextField
          fullWidth
          label="Project Name"
          name="name"
          value={projectData.name}
          onChange={handleChange}
          required
        />
        <TextField
          fullWidth
          label="Project Description"
          name="description"
          value={projectData.description}
          onChange={handleChange}
          multiline
          rows={4}
          required
        />
        <FormControl fullWidth>
          <InputLabel id="contributors-label">Contributors</InputLabel>
          <Select
            labelId="contributors-label"
            multiple
            value={projectData.contributors}
            onChange={handleContributorsChange}
            renderValue={(selected) => selected.map(id => users.find(user => user.id === id)?.username).join(', ')}
          >
            {users.map((user) => (
              <MenuItem key={user.id} value={user.id}>
                <Checkbox checked={projectData.contributors.indexOf(user.id) > -1} />
                <ListItemText primary={user.username} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <TextField
          fullWidth
          label="Task Title"
          name="taskTitle"
          value={projectData.taskTitle}
          onChange={handleChange}
          required
        />
        <TextField
          fullWidth
          label="Task Description"
          name="taskDescription"
          value={projectData.taskDescription}
          onChange={handleChange}
          multiline
          rows={4}
          required
        />
        <FormControl fullWidth>
          <InputLabel id="assigned-to-label">Task Assigned To</InputLabel>
          <Select
            labelId="assigned-to-label"
            name="taskAssignedTo"
            value={projectData.taskAssignedTo}
            onChange={handleChange}
            required
          >
            {users.map((user) => (
              <MenuItem key={user.id} value={user.id}>
                {user.username}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={loading}
          className="w-full"
        >
          {loading ? <CircularProgress size={24} /> : 'Create Project'}
        </Button>
      </form>
    </div>
  );
}

export default CreateProject;