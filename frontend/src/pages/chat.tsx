import '../styles/chat.css'
import { Context } from '../components/presentationCard.tsx'
import type { ContextProps } from '../components/presentationCard.tsx'
import type { ChatbotBubbleProps } from '../components/chatBubble.tsx'
import type { messageType } from '../components/types.ts'
import type { ComponentType, Dispatch, SetStateAction } from 'react'

interface ChatProps extends ContextProps {
    ChatbotBubble: ComponentType<ChatbotBubbleProps>;
    tpId: string;
    message: messageType[];
    input: string;
    loading: boolean;
    setMessage: Dispatch<SetStateAction<messageType[]>>;
    setInput: Dispatch<SetStateAction<string>>;
    setLoading: Dispatch<SetStateAction<boolean>>;
    setTitle: Dispatch<SetStateAction<string>>;
    setSubject: Dispatch<SetStateAction<string>>;
    setObject: Dispatch<SetStateAction<string>>;
    addContext: (newTitle: string, newSubject: string, newObject: string, newDate: { date: string; heure: string }) => void;
    sendActive: boolean;
    setSendActive: Dispatch<SetStateAction<boolean>>;
    contextOpen: boolean;
    setContextOpen: Dispatch<SetStateAction<boolean>>;
}
   

export function Chat ({
    subject, setSubject, title,
    setTitle, object, setObject, tpId,
    addContext, contextOpen,
    setContextOpen, ChatbotBubble, message,
    input, loading, setMessage, setInput, setLoading, sendActive, setSendActive
}: ChatProps) {


    return (
        <div className='chat-main-container'>
            {contextOpen? (
                <div>
                    <Context subject={subject} setSubject={setSubject} title={title} setTitle={setTitle} object={object} setObject={setObject} setMessage={setMessage} addContext={addContext} setContextOpen={setContextOpen} />
                </div>
            ): (
                <div className='chatbot-container'>
                    <ChatbotBubble message={message} setMessage={setMessage} input={input} setInput={setInput} loading={loading} setLoading={setLoading} sendActive={sendActive} setSendActive={setSendActive} chatContext={{ id: tpId, subject, title, object }} />
                </div>
            )}
        </div>
    )
}