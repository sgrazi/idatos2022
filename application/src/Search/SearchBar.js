import { useState } from "react";
import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";
import TextField from "@mui/material/TextField";
import axios from "axios";

const FORM_ENDPOINT = "http://localhost:5001/movies";

const SearchBar = ({setMovies}) => {
  const [title, setTitle] = useState("")
  const handleTitle = (e) => {
    setTitle(e.target.value)
  }
  
  const handleSubmit = () => {
    axios.post(FORM_ENDPOINT, null, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      params: {
        title
      }
    })
      .then(response => {
        setMovies(response.data.movies)
      })
      .catch(err => console.log(err))
  };

  return (
    <div 
      style={{ width: "100%", paddingBottom: 20}}
    >
      <TextField
        style={{width: "95%"}}
        value={title}
        onChange={handleTitle}
        className="text"
        name="title"
        label="Busca una pelicula por nombre"
        placeholder="Ingresa un nombre..."
        size="large"
        variant="outlined"
        required
      />
      <IconButton onClick={handleSubmit} aria-label="search">
        <SearchIcon style={{ 
          paddingLeft: "9",
          fill: "white"
        }} />
      </IconButton>
    </div>
  )
};

export default SearchBar