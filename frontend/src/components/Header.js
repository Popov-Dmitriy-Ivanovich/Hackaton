import React, {Component} from 'react'
import './Header.css'

class Header extends Component{
    render(){
        return(
            <div className='Header'>
                <div className='Name' onClick={()=>this.props.go_to_menu()}>
                    Career Guider
                </div>
                <span className='HeaderRightPart'>
                    {this.props.show_menu_button ? 
                    <div className='MenuButton' onClick={()=>this.props.go_to_menu()}>
                        Меню
                    </div>:''}
                    {this.props.show_logout ? 
                    <div className='LogoutButton' onClick={()=>this.props.logout()}>
                        Выйти
                    </div>:''}
                </span>
                    
            </div>
        )
    }
}

export default Header;