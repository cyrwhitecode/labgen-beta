import { Outlet } from 'react-router-dom'
import { Header } from '../components/header.tsx'
import '../styles/layout.css'

export function Layout () {

    return (
        <div>
            <header>
                <Header />
            </header>

            <main>
                <Outlet />
            </main>
        </div>
    )
}