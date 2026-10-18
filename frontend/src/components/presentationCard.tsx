import '../styles/presentationCard.css'
//import { useState } from 'react'
import type { ContextType, DateType, messageType as ChatMessage } from './types.ts'
export type { ContextType } from './types.ts'

export interface messageType {
    
}

// Dashboard components
export function GeneratedReport () {

    return (
        <div className='genr-container'>
            <div className='genr-l1'>
                <code>XX</code>
                <p>Rapport generes</p>
            </div>
            <div className='acc-container'>
                <button className='genr-btn'>Acc</button>
                <div className='voyant'></div>
            </div>
        </div>
    )
}

export function HomeCard({ newTP }: AddTPProps) {
    
    return (
        <div className="home-card-container container">
            <div>
                <code className='home-code'>Assistant de laboratoire</code>
            </div>
            <div className='home-l2'>
                <h1>Prepare & analyse tes TP en 30 secondes.</h1>
                <p>Importe tes mesures, LabGen calcule les regressions, incertitudes et redige ton compte rendu.</p>
            </div>
            <button className='home-btn' onClick={newTP}>+ Creer un nouveau TP</button>
        </div>
    )
}

export interface HistoryCardProps {
    contextList: ContextType[];
    deleteContext: (id: string) => void;
    openContext: (id: string) => void;
}

export interface AddTPProps {
    newTP: () => void;
}

export interface ContextProps {
    subject: string;
    setSubject: React.Dispatch<React.SetStateAction<string>>;
    title: string;
    setTitle: React.Dispatch<React.SetStateAction<string>>;
    object: string;
    setObject: React.Dispatch<React.SetStateAction<string>>;
    setMessage: React.Dispatch<React.SetStateAction<ChatMessage[]>>;
    addContext: (title: string, subject: string, object: string, date: DateType) => void;
    setContextOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

export function HistoryCard ({ contextList, deleteContext, openContext }: HistoryCardProps) {

    // Matiere color style
    const getSubjectStyle = (subj: string): string => {
        if (subj === "Physique") return "physique standard"
        if (subj === "Chimie") return "chimie standard"
        if (subj === "SVT") return "SVT standard"
        return "other standard"
    }

    return (
        <div className='main-history-container'>
            {
                contextList.map((tp) => (
                    <div key={tp.id} className='history-card-container container'>
                        <div className='history-l1'>
                            <code className={getSubjectStyle(tp.subject)}>{tp.subject}</code>
                            <code className='date'>{tp.date?.date} - {tp.date?.heure}</code>
                        </div>
                        <div className='history-l2'>
                            <h3>{tp.title}</h3>
                            <div className='history-l2-1'>
                                <p>{tp.object? tp.object.slice(0, 90): tp.object} .....</p>
                                <code onClick={() => deleteContext(tp.id)}>Delete</code>
                            </div>
                        </div>
                        <div className='history-l3'>
                            <button className='history-btn' onClick={() => openContext(tp.id)}>Conversation</button>
                            <button className='history-btn'>PDF</button>
                        </div>
                    </div>
                ))
            }
        </div>
    )
}

export function AddTP ({ newTP }: AddTPProps) {

    return (
        <div className='add-tp-container container'>
            <button onClick={() => newTP()} className='add-btn'>+</button>
            <p>Nouveau TP</p>
        </div>
    )
}

// Chat components
export function Context ({ 
        subject, setSubject, title, setTitle, object, setObject, addContext, setContextOpen
    }: ContextProps) {

    const handleSubject = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSubject(e.target.value)
    }
    const handleTitle = (e: React.ChangeEvent<HTMLInputElement>) => {
        setTitle(e.target.value)
    }
    const handleObject = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setObject(e.target.value)
    }
    const getDate = (): DateType => {
        const d = new Date()
        const heure = d.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })
        const date = d.toLocaleDateString("fr-FR")
        const timeTP: DateType = { date: date, heure: heure }
        return timeTP
    }

    const handleSubmitContext = (e: React.MouseEvent<HTMLButtonElement>) => {
        if (subject==="" || object==="" || title==="") {
            alert("Veillez vous assurer vous que tous les champs sont remplis")
        } else {
            e.preventDefault()
            addContext(title, subject, object, getDate())
            setContextOpen(false)
        }
    }

    return (
        <div className="context-container container">
            <div className='context-l1'>
                <code>Renseignements IA</code>
                <h2>Context du TP</h2>
                <p>Donne les grandes lignes de ton TP. LabGen s'en sert pour rediger l'introduction et l'analyse.</p>
            </div>
            <div className='context-l2'>
                <code>Titre de TP</code>
                <input onChange={handleTitle} value={title} type="text" placeholder="Ex. La viscosimetrie" />
            </div>
            <div className='context-l3'>
                <code>Matiere</code>
                <div  className='check-field'>
                    <label><input onChange={handleSubject} checked={subject === "Physique"} type="radio" value="Physique" /> Physique</label>
                    <label><input onChange={handleSubject} checked={subject === "Chimie"} type="radio" value="Chimie" /> Chimie</label>
                    <label><input onChange={handleSubject} checked={subject === "SVT"} type="radio" value="SVT" /> SVT</label>
                    <label>Autre <input onChange={handleSubject} className="autre" type="text" value={subject} placeholder="Autre" /></label>
                </div>
            </div>
            <div className='context-l4'>
                <code>Instructions ou bjectifs du TP</code>
                <div className='instruction-field'>
                    <textarea onChange={handleObject} value={object} rows={5} placeholder="Entrer l'hypothese a verifier (principe), le materiel et la methode experimentale ..." />
                    <button className='micro-btn-context'>M</button>
                </div>
            </div>
            <button onClick={handleSubmitContext} className='continue'>Continuer</button>
        </div>
    )
}

export function ChatSpace () {

    return (
        <div>
            CHAT SPACE
        </div>
    )
}

/*export function AiField ({ setMessage, message, sendActive }) {

    const handleChangeMessage = (e) => {
        setMessage(e.target.message)
    }
    const handleSubmitMessage = (e) => {
        e.preventDefault()
        //sendToAI(message)
    }

    return (
        <div className='ai-main-container'>
            <div className='ai-field-container'>
                <textarea onChange={handleChangeMessage} value={message} rows="10" placeholder="Ecrivez a LabGen ..." />
                <button className='import-file'>+</button>
                {sendActive? <button className='send'>S</button>: null}
                <button className='ai-micro'>M</button>
            </div>
        </div>
    )
}*/


export function Loading () {

    return (
        <div className='loading-container container'>
            <div>
                <div>
                    LOADING STATE ....
                </div>
                <code>n% . Generation de ton rapport</code>
            </div>
            <div>
                <p>Nettoyage des donnees</p>
                <p>Calculs mathematiques & regression lineare</p>
                <p>Redaction du texte par L'IA</p>
                <p>Compilation du PDF</p>
            </div>
            <div>
                <p>Ne ferme pas cette fenetre - Ton rapport arrive dans quelaues temps.</p>
            </div>
        </div>
    )
}

// VISUALIZATION COMPONENTS
export function keyResults () {
    return (
        <div className='results-container container'>
            Results...
        </div>
    )
}

export function Options () {
    return (
        <div className='option-container container'>
            <button>Telecharger PDG pret a imprimer</button>
            <button>Partager sur WhatsApp</button>
            <button>Modifier les donnees</button>
        </div>
    )
}

export function Details () {
    return (
        <div className='detail-container container'>
            <h3>Details</h3>
            <div>
                <p>Format</p>
                <p>.....</p>
            </div>
            <div>
                <p>Theme</p>
                <p>.....</p>
            </div>
            <div>
                <p>Taille fichier</p>
                <p>.....</p>
            </div>
            <div>
                <p>Generation</p>
                <p>.....</p>
            </div>
        </div>
    )
}