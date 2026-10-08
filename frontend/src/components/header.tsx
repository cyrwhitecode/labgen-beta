import { NavLink } from 'react-router-dom'
import '../styles/header.css'

export function Header () {

    const navStyle = ({isActive}: {isActive: boolean}) => isActive? "isActive none": "noActive none"

    return (
        <div className='header-container'>
            <div className='logo-container'>
                <h2>LabGen</h2>
                <div className='sub-container'>
                    <div className='voyant2'></div>
                    <code className='beta'>Beta</code>
                </div>
            </div>
            <nav className='mobile-container'>
                <NavLink className={navStyle} to='/'>DashBoard</NavLink>
                <NavLink className={navStyle} to='/chat'>Chat</NavLink>
                <NavLink className={navStyle} to='/rapports'>Rapports</NavLink>
            </nav>
        </div>
    )
}