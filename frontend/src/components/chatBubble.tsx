import '../styles/presentationCard.css'
import '../styles/chatbotBubble.css'
import { useEffect, useRef, useState, type Dispatch, type SetStateAction } from 'react'
import 'katex/dist/katex.min.css'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeKatex from 'rehype-katex'
import remarkMath from 'remark-math'
import type { ContextType, messageType } from './types.ts'

export interface chatType {
    user: string;
    ai: string;
}
export type { messageType } from './types.ts'

export interface ChatbotBubbleProps {
    chatContext: Pick<ContextType, 'id' | 'subject' | 'title' | 'object'>;
    sendActive: boolean;
    setSendActive: Dispatch<SetStateAction<boolean>>;
    message: messageType[];
    setMessage: Dispatch<SetStateAction<messageType[]>>;
    input: string;
    setInput: Dispatch<SetStateAction<string>>;
    loading: boolean;
    setLoading: Dispatch<SetStateAction<boolean>>;
}

export function ChatbotBubble ({ 
    chatContext, sendActive, setSendActive, message, setMessage, input, 
    setInput, loading, setLoading }: ChatbotBubbleProps) {
    const endOfMessagesRef = useRef<HTMLDivElement | null>(null)
    const chatRequestRef = useRef<AbortController | null>(null)
    const storageKey = `labgen:chat${chatContext.id}`;
    const [loadedKey, setLoadedKey] = useState<string>("");

    useEffect(() => {
        try {
            const saved = localStorage.getItem(storageKey);
            setMessage(saved ? JSON.parse(saved) : [{ sender: "assistant", content: "Bonjour, comment avance ton projet de TP?" }]);
        } catch (error) {
            console.error('Erreur lors du chargement des messages depuis le localStorage:', error);
            setMessage([]);
        }
        setLoadedKey(storageKey);
    }, [storageKey]);

    useEffect(() => {
        if (loadedKey !== storageKey) return;
        localStorage.setItem(storageKey, JSON.stringify(message));
    }, [message, storageKey, loadedKey]);

    useEffect(() => () => chatRequestRef.current?.abort(), [])

    useEffect(() => {
        if (input.trim() !== "") {
            setSendActive(true)
        }
    }, [input, setSendActive])

    const sendMessage = async () => {
        if (!sendActive) return;

        const trimmedInput = input.trim();
        if (!trimmedInput) return;

        const userMessage: messageType = { sender: 'user', content: trimmedInput }
        const updatedMessages = [...message, userMessage]

        setMessage(updatedMessages)
        setInput("")
        setLoading(true)
        const requestController = new AbortController()
        chatRequestRef.current = requestController

        try {
            const response = await fetch('http://127.0.0.1:8000/chat', {
                method: 'POST',
                headers: { 'content-type': 'application/json' },
                signal: requestController.signal,
                body: JSON.stringify({
                    context: chatContext,
                    messages: [...message, userMessage]
                        .slice(-20)
                        .map(({ sender, content }) => ({ role: sender, content }))
                })
            })

            if (!response.ok) {
                throw new Error(`Erreur API: ${response.status} ${response.statusText}`)
            }

            const data = await response.json()
            const reply = typeof data?.reply === 'string'
                ? data.reply
                : typeof data?.message === 'string'
                    ? data.message
                    : typeof data?.answer === 'string'
                        ? data.answer
                        : 'Je n\'ai pas reçu de réponse valide.'

            const assistantMessage: messageType = { sender: 'assistant', content: reply }
            setMessage((prev: messageType[]) => [...prev, assistantMessage])
        } catch (error) {
            if (error instanceof DOMException && error.name === 'AbortError') return
            console.error('Erreur lors de la réponse de l\'IA:', error)
            setMessage((prev: messageType[]) => [
                ...prev,
                { sender: 'assistant', content: 'Désolé, je n\'ai pas pu obtenir de réponse de l\'IA. Vérifie le backend /api/chat et la console du navigateur.' }
            ])
        } finally {
            if (chatRequestRef.current === requestController) {
                chatRequestRef.current = null
                setLoading(false)
            }
        }
    }


    useEffect(() => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
    }, [message, loading])


    return (
        <div className='chat-bubble-container'>
            <div className='chat-container'>
                <div className='chat-container-0'>
                    {message.map((msg, index) => (
                        <div key={`${msg.sender}-${index}`} className='chat-container-1'
                            style={{
                                justifyContent: msg.sender==='assistant'? 'flex-start': 'flex-end',
                            }}>
                            <div className='content'
                                style={{
                                   background: msg.sender==='assistant'? 'rgba(78, 81, 90, 0.45)': 'rgba(15, 37, 119, 0.45)', 
                                   borderRadius: msg.sender==='assistant'? '0 10px 10px 10px': '10px 0 10px 10px',
                                }}>
                                <div className='markdown-body'>
                                    <ReactMarkdown
                                        remarkPlugins={[[remarkMath, { singleDollar: true }], remarkGfm]}
                                        rehypePlugins={[[rehypeKatex, { output: 'htmlAndMathml', strict: false }]]}
                                    >
                                        {msg.content}
                                    </ReactMarkdown>
                                </div>
                                <div className='message-copy-options'>
                                    <details>
                                        <summary>Copier</summary>
                                        <div className='message-copy-menu'>
                                            <button type='button'>
                                                Texte rendu
                                            </button>
                                            <button type='button'>
                                                Source Markdown
                                            </button>
                                        </div>
                                    </details>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
                {loading && (<div>L'assistant reflechit...</div>)}
                <div ref={endOfMessagesRef} className="chat-end-anchor" />
            </div>

            <div className='ai-main-container'>
                <div className='ai-field-container'>
                    <textarea
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                sendMessage();
                            }
                        }}
                        value={input}
                        rows={10}
                        placeholder="Ecrivez a LabGen ..." 
                    />
                    <button type='button' className='import-file'>+</button>
                    {sendActive ? <button type='button' onClick={sendMessage} className='send'>S</button> : null}
                    <button type='button' className='ai-micro'>M</button>
                </div>
            </div>
        </div>
    )
}
