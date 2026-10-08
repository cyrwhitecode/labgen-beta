import { 
    HomeCard,
    HistoryCard,
    AddTP
 } from '../components/presentationCard.tsx'
import '../styles/dashboard.css' 
import type { ContextType } from '../components/presentationCard.tsx'

interface DashboardProps {
    contextList: ContextType[];
    newTP: () => void;
    deleteContext: (id: string) => void;
    openContext: (id: string) => void;
}

export function Dashboard ({ contextList, newTP, deleteContext, openContext }: DashboardProps) {

    const listLenght = (list: ContextType[]) => {
        if (list.length === 0) return "Aucun TP"
        if (list.length === 1) return "1 TP"
        if (list.length > 1) return `${contextList.length} Travaux pratiques`
    }

    return (
        <div className='dashboard-container'>
            <HomeCard newTP={newTP} /> 
            <div className='history-main-container'>
                <div className='history0-l1'>
                    <h3>History</h3>
                    <code>{listLenght(contextList)}</code>
                </div>
                <div className='history0-l2'>
                    <HistoryCard contextList={contextList} deleteContext={deleteContext} openContext={openContext} />
                    <div>
                        <AddTP newTP={newTP} />
                    </div>
                </div>
            </div>
        </div>
    )
}