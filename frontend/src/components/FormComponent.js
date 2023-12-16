import React, {Component} from 'react'
import './FormComponent.css'

class FormComponent extends Component{
    state={
        subforms: [],
        choices: [],
        form_was_sended: 'not',
        form_error_description: ''
    }
    constructor(props){
        super(props);
    }

    buttons_listener = (text, value, type) => {
        let tmp=this.state.choices;
        tmp[text]=value;
        if (type === "checkbox" && value==='-'){
            delete tmp[text]
        }
        this.setState({choices: tmp});
    }

    componentDidMount() {
        fetch(this.props.main_host+this.props.form_route)
        .then(res => res.json())
        .then(
            (result) => {
                this.setState({
                    loaded: true,
                    subforms: result,
                    choices: {}
                });
            },
            (error) => {
                this.setState({
                    loaded: true,
                    error
                })
            }
        )
    }

    SendForm = async() => {
        if (Object.keys(this.state.choices).length<4 && Object.keys(this.state.choices).length>0)
        {
            await fetch(this.props.main_host + this.props.response_route, {
                method: 'POST',
                headers:{
                    'content-type': 'application/json;charser=utf-8'
                },
                body: JSON.stringify({"login": this.props.login, "choises": Object.keys(this.state.choices)}),
            })
            .then(responce => {
                responce.json().then(res=>{
                if (res.status === 'OK'){
                    this.setState({form_was_sended: 'success'})
                }
                else{
                    this.setState({form_was_sended: 'failed'})
                }
                })
                
            })
        }
        else{
            this.setState({form_was_sended: 'failed'})
            this.setState({form_error_description: 'Количество ответов должно быть от 1 до 3'})
        }
        
    }

    reset_form = () => {
        this.setState({
            choices: [],
            form_was_sended: 'not',
            form_error_description: ''
        })
    }

    render(){
        return(
            <div>
                <div className='ResultDiv' style={{display: !(this.state.form_was_sended==='not') ? '' : 'none' }}>
                    {/* <div className='FormErrorContainer'> */}
                        {this.state.form_was_sended==='success'? 'Форма отправлена успешно' : ''}
                        {this.state.form_was_sended==='failed' ? <div><span className='FormErrorLable'>Произошла ошибка</span> <br/> <span className='FormErrorDescription'>{this.state.form_error_description}</span><br/><button className='DropFormButton' onClick={this.reset_form}>Заполнить форму заново</button></div>         : ''}
                    {/* </div> */}
                </div>
                <div className='FormContainer' style={{display: (this.state.form_was_sended==='not') ? '' : 'none' }}>
                    <ul className="Form_ul">
                        {this.state.subforms.map((subform)=>(
                            <li>
                                <div className='subform_container'>
                                <div className='subform_lable'>{subform.text}</div>
                                {
                                    <ul style={{listStyle: 'none', paddingInlineStart: 'clamp(10px, 5vw, 40px)'}}>
                                        {subform.buttons.buttons_texts.map((text)=>(
                                            <li>
                                                <label className='LableInput'><input
                                                    className='FormInput'
                                                    type={subform.buttons.buttons_type} 
                                                    name={subform.text} 
                                                    onChange={
                                                        (subform.buttons.buttons_type==="radio") ? 
                                                            ()=>this.buttons_listener(subform.text, text, subform.buttons.buttons_type) 
                                                        : (subform.buttons.buttons_type==="checkbox") ? 
                                                            ()=>this.buttons_listener(text, this.state.choices[text]==='+' ? '-' : '+', subform.buttons.buttons_type)
                                                        : (subform.buttons.buttons_type==="text") ? 
                                                            (event)=>{this.buttons_listener(subform.text, event.target.value, subform.buttons.buttons_type); this.change_text_input(subform.text, event.target.value)} 
                                                        :
                                                            ()=>{}}
                                                >
                                                </input><span className='ButtonText'>{text}</span></label>
                                            </li>
                                        ))}
                                    </ul>
                                }
                                </div>
                            </li>
                        ))}
                    </ul>
                </div>
                <span className='SendFormButtonContainer' style={{display: (this.state.form_was_sended==='not') ? '' : 'none' }}><button className='SendFormButton' onClick={this.SendForm}>Send form</button></span>
            </div>
        )
    }
}
export default FormComponent;