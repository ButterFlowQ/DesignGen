package com.example.projectname.service;

import com.example.projectname.entities.User;
import com.example.projectname.enums.UserRole;
import com.example.projectname.repository.UserRepository;
import com.example.projectname.security.JwtTokenProvider;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.sql.Timestamp;
import java.util.UUID;

/**
 * AuthService handles business logic related to user authentication,
 * including registration, login, and logout operations.
 */
@Service
public class AuthService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private JwtTokenProvider jwtTokenProvider;

    /**
     * Registers a new user with the provided details.
     *
     * @param username the username of the new user
     * @param email    the email of the new user
     * @param password the password of the new user
     * @param role     the role of the new user
     * @return the registered User entity
     */
    public User register(String username, String email, String password, UserRole role) {
        if (userRepository.findByEmail(email).isPresent()) {
            throw new IllegalArgumentException("Email already in use");
        }

        User user = new User();
        user.setUsername(username);
        user.setEmail(email);
        user.setPassword(passwordEncoder.encode(password));
        user.setRole(role);
        user.setTokenVersion(0);
        long now = System.currentTimeMillis();
        user.setCreatedAt(new Timestamp(now));
        return userRepository.save(user);
    }

    /**
     * Authenticates a user and returns a JWT token.
     *
     * @param email    the email of the user
     * @param password the password of the user
     * @return a JWT token if authentication is successful
     */
    public String login(String email, String password) {
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new IllegalArgumentException("Invalid email or password"));
        if (!passwordEncoder.matches(password, user.getPassword())) {
            throw new IllegalArgumentException("Invalid email or password");
        }
        return jwtTokenProvider.createToken(user.getId(), user.getRole(), user.getTokenVersion());
    }

    public void logout(String token) {
        UUID userId = jwtTokenProvider.getUserIdFromToken(token);
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("User not found"));
        user.setTokenVersion(user.getTokenVersion() + 1);
        userRepository.save(user);
    }
}