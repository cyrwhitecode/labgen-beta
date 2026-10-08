import { useEffect, useState } from 'react'
import { Routes, Route, useNavigate } from 'react-router-dom'
import { Layout } from './layout/layout.tsx'
import { Dashboard } from './pages/dashboard.tsx'
import { Chat } from './pages/chat.tsx'
import { Rapports } from './pages/rapports.tsx'
import { ChatbotBubble } from './components/chatBubble.tsx'
import type { ContextType, messageType } from './components/types.ts'
import './styles/App.css'

function App() {
  const [subject, setSubject] = useState<string>("")
  const [title, setTitle] = useState<string>("")
  const [object, setObject] = useState<string>("")
  const [tpId, setTpId] = useState<string>(() => crypto.randomUUID())
  const [contextList, setContextList] = useState<ContextType[]>(() => {
    try {
      const savedList = localStorage.getItem("labgenTP");
      return savedList? JSON.parse(savedList): [];
    } catch {
      return []
    }
  })
  const [contextOpen, setContextOpen] = useState<boolean>(false)
  const [sendActive, setSendActive] = useState<boolean>(false)
  

  const [message, setMessage] = useState<messageType[]>([
    { sender: "assistant", content: "Bonjour, comment avance ton projet de TP?" }
  ])
  const [input, setInput] = useState<string>("")
  const [loading, setLoading] = useState<boolean>(false)

  const navigate = useNavigate()

  const addContext = (newTitle: string, newSubject: string, newObject: string, newDate: { date: string; heure: string }) => {
    const newContext:ContextType = {
      id: tpId,
      title: newTitle,
      subject: newSubject,
      object: newObject,
      date: newDate,
      messages: [...message]
    }
    setContextList((prevContexts) => [...prevContexts, newContext])
  }

  const newTP = () => {
    setTpId(crypto.randomUUID())
    setSubject("")
    setTitle("")
    setObject("")
    setContextOpen(true)
    setMessage([{ sender: 'assistant', content: 'Bonjour, comment avance ton projet de TP?' }])
    navigate('/chat')
  }

  const deleteContext = (id: string) => {
    setContextList((prevList) => prevList.filter((context) => context.id !== id))
  }

  const openContext = (id: string) => {
    const context = contextList.find((item) => item.id === id)
    if (!context) return
    setTpId(context.id)
    setSubject(context.subject)
    setTitle(context.title)
    setObject(context.object)
    setMessage([...context.messages])
    setContextOpen(false)
    navigate('/chat')
  }

  useEffect(() => {
    localStorage.setItem("labgenTP", JSON.stringify(contextList))
  }, [contextList])

  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path='/' element={<Dashboard contextList={contextList} newTP={newTP} deleteContext={deleteContext} openContext={openContext} />} />
        <Route path='/chat' element={<Chat ChatbotBubble={ChatbotBubble} subject={subject} setSubject={setSubject} title={title}
            setTitle={setTitle} object={object} setObject={setObject} tpId={tpId} addContext={addContext} contextOpen={contextOpen} setContextOpen={setContextOpen}
            message={message} setMessage={setMessage} sendActive={sendActive} setSendActive={setSendActive}
            input={input} setInput={setInput} loading={loading} setLoading={setLoading} />}/>
        <Route path='/rapports' element={<Rapports />} />
      </Route>
    </Routes>
  )
}

export default App
