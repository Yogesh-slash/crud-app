import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [notes, setNotes] = useState([]);
  const [content, setContent] = useState('');

  useEffect(() => {
    fetchNotes();
  }, []);

  const fetchNotes = async () => {
    const res = await axios.get('http://localhost:5000/api/notes');
    setNotes(res.data);
  };

  const addNote = async () => {
    if (!content.trim()) return;
    const res = await axios.post('http://localhost:5000/api/notes', { content });
    setNotes([...notes, res.data]);
    setContent('');
  };

  const deleteNote = async (id) => {
    await axios.delete(`http://localhost:5000/api/notes/${id}`);
    setNotes(notes.filter(note => note.id !== id));
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Notes App</h2>
      <input
        type="text"
        value={content}
        onChange={e => setContent(e.target.value)}
        placeholder="Enter a note"
      />
      <button onClick={addNote}>Add Note</button>
      <ul>
        {notes.map(note => (
          <li key={note.id}>
            {note.content} <button onClick={() => deleteNote(note.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;