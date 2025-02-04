package com.example.projectname.controller;

import com.example.projectname.entities.User;
import com.example.projectname.service.ShopkeeperService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * Controller managing operations related to shopkeepers, including retrieving the list of shopkeepers.
 */
@RestController
public class ShopkeeperController {

    @Autowired
    private ShopkeeperService shopkeeperService;

    /**
     * Retrieves a list of all shopkeepers available on the platform.
     *
     * @return ResponseEntity containing the list of shopkeepers.
     */
    @GetMapping("/shopkeepers")
    public ResponseEntity<List<User>> getAllShopkeepers() {
        List<User> shopkeepers = shopkeeperService.getAllShopkeepers();
        return ResponseEntity.ok(shopkeepers);
    }
}