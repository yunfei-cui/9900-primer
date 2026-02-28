import { useState, useEffect } from 'react'
import { getStudents, createStudent, updateStudent, deleteStudent, getStats } from './api'
import StudentForm from './components/StudentForm'
import StudentTable from './components/StudentTable'
import EditStudentModal from './components/EditStudentModal'
import Stats from './components/Stats'
import './App.css'

export default function App() {
  const [students, setStudents] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [editing, setEditing] = useState(null)

  const load = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await getStudents()
      setStudents(data)
      const statsData = await getStats()
      setStats(statsData)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  const handleCreate = async (student) => {
    setError(null)
    try {
      const created = await createStudent(student)
      setStudents((prev) => [...prev, created])
      const statsData = await getStats()
      setStats(statsData)
    } catch (e) {
      setError(e.message)
    }
  }

  const handleUpdate = async (id, student) => {
    setError(null)
    try {
      const updated = await updateStudent(id, student)
      setStudents((prev) => prev.map((s) => (s.id === id ? updated : s)))
      const statsData = await getStats()
      setStats(statsData)
      setEditing(null)
    } catch (e) {
      setError(e.message)
    }
  }

  const handleDelete = async (id) => {
    setError(null)
    try {
      await deleteStudent(id)
      setStudents((prev) => prev.filter((s) => s.id !== id))
      const statsData = await getStats()
      setStats(statsData)
      if (editing?.id === id) setEditing(null)
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Student Marks Manager</h1>
        <p className="tagline">Create and manage students and their marks</p>
      </header>

      <main className="main">
        <section className="card form-card">
          <h2>Add tutor</h2>
          <StudentForm onSubmit={handleCreate} />
        </section>

        {error && (
          <div className="banner banner-error" role="alert">
            {error}
          </div>
        )}

        {!loading && stats && (
          <section className="card stats-card">
            <h2>Statistics</h2>
            <Stats stats={stats} />
          </section>
        )}

        <section className="card table-card">
          <h2>Tutors</h2>
          {loading ? (
            <p className="loading">Loading…</p>
          ) : (
            <StudentTable
              students={students}
              onEdit={setEditing}
              onDelete={handleDelete}
            />
          )}
        </section>
      </main>

      {editing && (
        <EditStudentModal
          student={editing}
          onSave={handleUpdate}
          onClose={() => setEditing(null)}
        />
      )}
    </div>
  )
}
