package com.example.projectname.service;

import com.example.projectname.entities.User;
import com.example.projectname.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.*;
import org.springframework.stereotype.Service;

import java.util.Collection;
import java.util.Collections;
import java.util.UUID;

/**
 * UserService handles user-related operations such as retrieving user details by ID
 * and integrating with Spring Security for authentication.
 */
@Service
public class UserService implements UserDetailsService {

    @Autowired
    private UserRepository userRepository;

    /**
     * Retrieves a user by their unique ID.
     *
     * @param userId the UUID of the user
     * @return the User entity
     * @throws UserNotFoundException if no user is found with the given ID
     */
    public User getUserById(UUID userId) throws UserNotFoundException {
        return userRepository.findById(userId)
                .orElseThrow(() -> new UserNotFoundException("User not found with ID: " + userId));
    }

    public User findByUserName(String username) {
        return userRepository.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found with username: " + username));
    }

    /**
     * Loads the user by username for Spring Security authentication.
     *
     * @param username the username identifying the user whose data is required.
     * @return a fully populated UserDetails object.
     * @throws UsernameNotFoundException if the user could not be found or has no GrantedAuthority.
     */
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        // You can modify this to use email or any other unique identifier
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found with username: " + username));

        return new org.springframework.security.core.userdetails.User(
                user.getUsername(),
                user.getPassword(),
                getAuthorities(user.getRole())
        );
    }

    /**
     * Converts the UserRole to a collection of GrantedAuthority.
     *
     * @param role the role of the user
     * @return a collection of GrantedAuthority
     */
    private Collection<? extends GrantedAuthority> getAuthorities(com.example.projectname.enums.UserRole role) {
        return Collections.singletonList(new SimpleGrantedAuthority("ROLE_" + role.name()));
    }

    /**
     * Exception thrown when a user is not found.
     */
    public static class UserNotFoundException extends RuntimeException {
        public UserNotFoundException(String message) {
            super(message);
        }
    }
}
