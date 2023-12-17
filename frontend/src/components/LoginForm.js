import React, {Component} from 'react';
import './LoginForm.css'

class LoginForm extends Component{

    state={
        login: '',
        password: '',
        name: '',
        logined: false,
        login_failed: false,
        register: false,
        registration_failed: false,
        registration_fail_code: '',
        registration_fail_codes:{
            'LogEx': 'Логин существует',
            'LogInc': 'Логин некорректный',
            'PasswInc': 'Пароль некорректный'
        }
    }

    send_login = async() => {
          
        await fetch(this.props.main_host + this.props.login_route, {
            method: 'POST',
            headers:{
                'content-type': 'application/json;charser=utf-8'
            },
            body: JSON.stringify({"login": this.state.login, "password": this.state.password}),
        })
        .then(responce => {
            responce.json().then(res=>{
                
            if (res.status === 'OK'){
                this.props.send_login(this.state.login, this.state.password);
                this.setState({logined: true})
            }
            else{
                this.setState({login_failed: true})
            }
            })
            
        })
    }

    login = () => {
        this.setState({register: false})
    }

    register = () => {
        this.setState({register: true})
    }

    send_register = async() => {
          
        await fetch(this.props.main_host + this.props.register_route, {
            method: 'POST',
            headers:{
                'content-type': 'application/json;charser=utf-8'
            },
            body: JSON.stringify({"login": this.state.login, "password": this.state.password, "name": this.state.name})
        })
        .then(responce => {
            responce.json().then(res=>{
            if (res.status === 'OK'){
                this.setState({register: false})
                
            }
            else{
                this.setState({registration_failed: true})
                this.setState({registration_fail_code: res.status})
            }
            })
            
        })
    }

    render(){
        return(
            <div className='LoginFormContainer'>
                <div className='LoginForm' onSubmit={()=>console.log('Submit')}>
                    
                    <span   style={{display: !this.state.register ? '' : 'none' }}    className='LoginLabel'>Login</span>
                    <span   style={{display:  this.state.register ? '' : 'none' }}    className='LoginLabel'>Register</span>
                    <form className='LoginForm_form'>
                    <input  style={{display:  this.state.register ? '' : 'none' }}    className='LoginFormInput NameInput'     placeholder='Name'                     onChange={(event)=>{this.setState({name: event.target.value})}}></input>
                    <input                                                            className='LoginFormInput LoginInput'    placeholder='Login' onChange={(event)=>{this.setState({login: event.target.value})}}></input>
                    <input                                                            className='LoginFormInput PasswordInput' placeholder='Password' type='password' onChange={(event)=>{this.setState({password: event.target.value})}} onKeyUp={(event)=>{if (event.key === "Enter") {this.state.register ? this.send_register() : this.send_login()}}}></input>
                    </form>
                    <p  style={{display:  this.state.register ? '' : 'none' }} className='RegisterDesc'>Логин, пароль и имя должны быть не длиннее 100 символов и содержатть только буквы латинского алфавита, цифры и символ нижнего подчёркивания ('_')</p>
                    
                    {(this.state.login_failed&&(!this.state.register)) ? <span className='LoginFailedLabel'>Login failed</span> :""}
                    {(this.state.registration_failed&&(this.state.register)) ? <div className='RegFailedContainer'> <div className='RegistrationFailedLabel'><span>Registration failed </span><br/><span className='RegistrationFailDescription'>{this.state.registration_fail_codes[this.state.registration_fail_code]}</span></div> </div>  :""}
                    <button style={{display: !this.state.register ? '' : 'none' }}    className='LoginButton'    onClick={()=>{this.send_login()}}>      Login    </button>
                    <button style={{display:  this.state.register ? '' : 'none' }}    className='LoginButton'    onClick={()=>{this.login()}}>           Login    </button>
                    <button style={{display: !this.state.register ? '' : 'none' }}    className='RegisterButton' onClick={()=>{this.register()}  }>      Register </button>
                    <button style={{display:  this.state.register ? '' : 'none' }}    className='RegisterButton' onClick={()=>{this.send_register()}  }> Register </button>
                </div>
            </div>
        )
    }
}

export default LoginForm;