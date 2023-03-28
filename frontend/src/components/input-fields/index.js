import React, { useState } from 'react'
import './index.scss'

const InputFields = () => {
  const [inputData, setInputData] = useState([
    {
      id: '1',
      value: '',
    },
    {
      id: '2',
      value: '',
    },
    {
      id: '3',
      value: '',
    },
    {
      id: '4',
      value: '',
    },
    {
      id: '5',
      value: '',
    },
    {
      id: '6',
      value: '',
    },
    {
      id: '7',
      value: '',
    },
  ])

  const inputFieldsData = [
    {
      label: 'Cement Component',
      placeholder: 'Enter the value of cement component',
    },
    {
      label: 'BlastFurnace Slag',
      placeholder: 'Enter the value of BlastFurnace Slag',
    },
    {
      label: 'Water Component',
      placeholder: 'Enter the value of WaterComponent',
    },
    {
      label: 'Super plasticizer Component',
      placeholder: 'Enter the value of Super plasticizer Component',
    },
    {
      label: 'Coarse Aggregate Component',
      placeholder: 'Enter the value of Coarse Aggregate Component',
    },
    {
      label: 'Fine Aggregate Component',
      placeholder: 'Enter the value of Fine Aggregate Component',
    },
    {
      label: 'AgeInDays',
      placeholder: 'Enter the value of AgeInDays',
    },
  ]

  const handleChangeInputData = (event, index) => {
    const newInput = [...inputData]
    newInput[index].value = event.target.value
    setInputData(newInput)
  }
  return (
    <div className="input">
      {inputFieldsData.map((item, index) => {
        return (
          <div className="input-container" key={index}>
            <label className="input__label">{item.label} : </label>
            <br />
            <input
              key={index}
              className="input__textfield"
              type="number"
              placeholder={item.placeholder}
              value={inputData.value}
              onChange={(event) => handleChangeInputData(event, index)}
            />
          </div>
        )
      })}
    </div>
  )
}

export default InputFields
