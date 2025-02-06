package com.example.projectname.repository;

import com.example.projectname.entities.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

/**
 * Repository interface for performing CRUD operations on User entities.
 */
@Repository
public interface UserRepository extends JpaRepository<User, UUID> {

    /**
     * Finds a user by their email address.
     *
     * @param email the email address of the user
     * @return an Optional containing the User if found, or empty if not
     */
    Optional<User> findByEmail(String email);

    Optional<User> findById(UUID id);

    Optional<User> findByUsername(String username);
}
