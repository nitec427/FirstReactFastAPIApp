import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Flex,
  Input,
  InputGroup,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Stack,
  Text,
  useDisclosure,
} from "@chakra-ui/react";
import {} from "bson-objectid";
var ObjId = require("bson-objectid");
const TodosContext = React.createContext({
  todos: [],
  fetchTodos: () => {},
});
function AddTodo() {
  const [date, setDate] = React.useState("");
  const [creator, setCreator] = React.useState("");
  const [title, setTitle] = React.useState("");
  const [body, setBody] = React.useState("");
  const [duration, setDuration] = React.useState("");
  const { todos, fetchTodos } = React.useContext(TodosContext);

  const handleDate = (event) => {
    setDate(event.target.value);
  };
  const handleCreator = (event) => {
    setCreator(event.target.value);
  };
  const handleTitle = (event) => {
    setTitle(event.target.value);
  };
  const handleBody = (event) => {
    setBody(event.target.value);
  };
  const handleDuration = (event) => {
    setDuration(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    fetchTodos();
    const newTodo = {
      created_date: date,
      creator: creator,
      title: title,
      body: body,
      duration: duration,
    };
    fetch("http://localhost:8000/todo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newTodo),
    }).then(fetchTodos);
  };

  return (
    <form onSubmit={handleSubmit} method="POST">
      <InputGroup size="md">
        <Input
          pr="4.5rem"
          type="text"
          placeholder="Enter the date of todo"
          aria-label="Enter to-do date"
          onChange={handleDate}
        />
        <Input
          pr="4.5rem"
          type="text"
          placeholder="Enter the creator of todo"
          aria-label="Enter to-do creator"
          onChange={handleCreator}
        />
        <Input
          pr="4.5rem"
          type="text"
          placeholder="Enter the title of todo"
          aria-label="Enter to-do title"
          onChange={handleTitle}
        />
        <Input
          pr="4.5rem"
          type="text"
          placeholder="Enter the body of todo"
          aria-label="Enter to-do body"
          onChange={handleBody}
        />
        <Input
          pr="4.5rem"
          type="text"
          placeholder="Enter the duration of todo"
          aria-label="Enter to-do duration"
          onChange={handleDuration}
        />
      </InputGroup>
      <button type="submit">Send</button>
    </form>
  );
}
export default function Todos() {
  const [todos, setTodos] = useState([]);
  const fetchTodos = async () => {
    const response = await fetch("http://localhost:8000/todo");
    const todos = await response.json();
    setTodos(todos);
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <TodosContext.Provider value={{ todos, fetchTodos }}>
      <AddTodo />
      <Stack spacing={5}>
        {todos.map((todo) => (
          <b>{todo["Title"]}</b>
        ))}
      </Stack>
      {}
    </TodosContext.Provider>
  );
}
