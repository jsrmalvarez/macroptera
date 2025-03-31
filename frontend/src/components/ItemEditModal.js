import React, { useState, useEffect } from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Button,
  FormControl,
  FormLabel,
  Input,
  Textarea,
  Switch,
  FormErrorMessage,
  useToast
} from '@chakra-ui/react';
import axios from 'axios';

const ItemEditModal = ({ isOpen, onClose, item, onUpdate }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    is_active: true
  });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const toast = useToast();

  // Update form data when item changes
  useEffect(() => {
    if (item) {
      setFormData({
        title: item.title || '',
        description: item.description || '',
        is_active: item.is_active || false
      });
    }
  }, [item]);

  const validateForm = () => {
    const newErrors = {};
    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = async () => {
    if (!validateForm() || !item) {
      return;
    }
    
    setIsSubmitting(true);
    try {
      const response = await axios.put(`http://localhost:8000/api/items/${item.id}`, formData);
      toast({
        title: 'Item updated',
        description: `${response.data.title} has been successfully updated`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      
      // Call the update handler with updated item
      onUpdate(response.data);
      
    } catch (error) {
      console.error('Error updating item:', error);
      toast({
        title: 'Error updating item',
        description: error.response?.data?.detail || error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Edit Item</ModalHeader>
        <ModalCloseButton />
        <ModalBody pb={6}>
          <FormControl isRequired isInvalid={!!errors.title} mb={4}>
            <FormLabel>Title</FormLabel>
            <Input
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              placeholder="Enter item title"
            />
            {errors.title && <FormErrorMessage>{errors.title}</FormErrorMessage>}
          </FormControl>

          <FormControl mb={4}>
            <FormLabel>Description</FormLabel>
            <Textarea
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              placeholder="Enter item description (optional)"
              resize="vertical"
            />
          </FormControl>

          <FormControl display="flex" alignItems="center" mb={4}>
            <FormLabel htmlFor="edit-is-active" mb="0">
              Active
            </FormLabel>
            <Switch
              id="edit-is-active"
              name="is_active"
              isChecked={formData.is_active}
              onChange={handleInputChange}
            />
          </FormControl>
        </ModalBody>

        <ModalFooter>
          <Button 
            colorScheme="blue" 
            mr={3} 
            onClick={handleSubmit}
            isLoading={isSubmitting}
          >
            Save
          </Button>
          <Button onClick={onClose}>Cancel</Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default ItemEditModal;