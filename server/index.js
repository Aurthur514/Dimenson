const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

const dbPath = path.join(__dirname, 'db.json');

// Get all todos
app.get('/todos', (req, res) => {
  fs.readFile(dbPath, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to read database' });
    }
    res.json(JSON.parse(data));
  });
});

// Add a new todo
app.post('/todos', (req, res) => {
  fs.readFile(dbPath, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to read database' });
    }
    const todos = JSON.parse(data);
    const newTodo = {
      id: Date.now(),
      text: req.body.text,
      completed: false,
    };
    todos.push(newTodo);
    fs.writeFile(dbPath, JSON.stringify(todos, null, 2), (err) => {
      if (err) {
        return res.status(500).json({ error: 'Failed to write to database' });
      }
      res.status(201).json(newTodo);
    });
  });
});

// Delete a todo
app.delete('/todos/:id', (req, res) => {
  const todoId = parseInt(req.params.id, 10);
  fs.readFile(dbPath, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to read database' });
    }
    let todos = JSON.parse(data);
    const initialLength = todos.length;
    todos = todos.filter((todo) => todo.id !== todoId);
    if (todos.length === initialLength) {
        return res.status(404).json({ error: 'Todo not found' });
    }
    fs.writeFile(dbPath, JSON.stringify(todos, null, 2), (err) => {
      if (err) {
        return res.status(500).json({ error: 'Failed to write to database' });
      }
      res.status(204).send();
    });
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
