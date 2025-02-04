package com.example.projectname.service;

import com.example.projectname.entities.User;
import com.example.projectname.enums.UserRole;
import com.example.projectname.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Service managing operations related to shopkeepers, such as retrieving all
 * shopkeepers.
 */
@Service
public class ShopkeeperService {

    @Autowired
    private UserRepository userRepository;

    /**
     * Retrieves a list of all shopkeepers available on the platform.
     *
     * @return a list of shopkeepers
     */
    public List<User> getAllShopkeepers() {
        return userRepository.findAll().stream()
                .filter(user -> user.getRole().equals(UserRole.SHOPKEEPER))
                .collect(Collectors.toList());
    }
}