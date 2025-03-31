import React from 'react';
import { Box, Container, Heading } from '@chakra-ui/react';
import ItemsList from './components/ItemsList';
import ItemForm from './components/ItemForm';

function App() {
  return (
    <Container maxW="container.xl" py={8}>
      <Heading as="h1" mb={6} textAlign="center">CRUD Application</Heading>
      <Box mb={10}>
        <ItemForm />
      </Box>
      <ItemsList />
    </Container>
  );
}

export default App;