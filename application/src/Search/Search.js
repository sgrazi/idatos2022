function search({ form, endpointUrl }) {

  const handleSubmit = (e) => {
    if (form) {
      e.preventDefault();

      const finalFormEndpoint = endpointUrl || form.action;
      const data = Array.from(form.elements)
        .filter((input) => input.name)
        .reduce(
          (obj, input) => Object.assign(obj, { [input.name]: input.value }),
          {}
        );

      fetch(finalFormEndpoint, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          if (response.status !== 200) {
            throw new Error(response.statusText);
          }

          return response.json();
        })
        .catch((err) => {
            console.log(err)
        });
    }
  };

  return { handleSubmit };
}

export default search;