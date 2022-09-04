import React from "react";
import { Heading, Flex, Divider } from "@chakra-ui/react";

const Header = () => {
  return (
    <Flex
      as="nav"
      align="center"
      justify="space-between"
      wrap="wrap"
      padding="0.5rem"
      bg="#ff4500"
      color="white"
      border="10px"
    >
      <Flex align="center" mr={5}>
        <Heading as="h2" size="sm">
          Istanbul Technical University
        </Heading>
        <Divider />
      </Flex>
    </Flex>
  );
};

export default Header;
