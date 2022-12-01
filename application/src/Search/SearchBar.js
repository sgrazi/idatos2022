import { useRef } from "react";
import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";
import TextField from "@mui/material/TextField";
import search from "./Search";

const FORM_ENDPOINT = "https:/localhost:5000/search/"; // TODO

const SearchBar = ({setSearchQuery}) => {
  const formElement = useRef(null);
  const handleSubmit = search({
    form: formElement.current
  });

  return (
    <form 
      action={FORM_ENDPOINT}
      onSubmit={handleSubmit}
      method="GET"
      target="_blank"
      ref={formElement}
      style={{ width: "100%", paddingBottom: 20}}
    >
      <TextField
        // color="white"
        style={{width: "95%"}}
        id="search-bar"
        className="text"
        onInput={(e) => {
          setSearchQuery(e.target.value);
        }}
        label="Busca una pelicula"
        variant="outlined"
        placeholder="Nombre..."
        size="large"
      />
      <IconButton type="submit" aria-label="search">
        <SearchIcon style={{ 
          paddingLeft: "9",
          fill: "white"
        }} />
      </IconButton>
    </form>
  )
};

export default SearchBar