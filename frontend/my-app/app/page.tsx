"use client"
import Image from "next/image";
import React,{useState} from "react";
import axios from "axios"


export default function Home() {

  const [selectedFile, setSelectedFile] = useState(null);
  const[text,setText]=useState(null)
  const[answer,setAnswer]=useState(null)

  const onTextChange=(event)=>{
    setText(event.target.value)

  }

  const onUploadText = async () => {
    const formData=new FormData();
    formData.append("text",text);
    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      body: formData
    });
    const data = await response.json();
    setAnswer(data.answer); 
  };

	const onFileChange = (event) => {
		const file=event.target.files[0];
    setSelectedFile(file);
	};
  const onFileUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }

  const formData=new FormData();
  formData.append("file",selectedFile)
  
  try {
    const response = await fetch("http://127.0.0.1:8000/uploadFile", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Upload failed");
    }

    const data = await response.json();
    console.log("Upload response:", data);
    alert(`File uploaded! Chunks count: ${data.chunks_count}`);
  } 
  catch (error) {
    console.error(error);
    alert("Error uploading file");
  }
  
};

  return (
    <div style={{padding:"40px"}}>
      <h2>Upload Document</h2>
      <input type="file" accept=".txt" onChange={onFileChange} />
      <button onClick={onFileUpload}>Upload</button>

      <h2 style={{ marginTop: "30px" }}>Ask Question</h2>
      <input
        style={{padding:"5px",margin:"5px"}}
        type="text"
        placeholder="Ask something..."
        value={text}
        onChange={onTextChange}
      />
      <button onClick={onUploadText}>Ask</button>

      {answer && (
        <div style={{ marginTop: "20px", border: "1px solid gray", padding: "10px" }}>
          <h3>Answer</h3>
          <p>{answer}</p>
        </div>
      )}
  </div>
  );
}
