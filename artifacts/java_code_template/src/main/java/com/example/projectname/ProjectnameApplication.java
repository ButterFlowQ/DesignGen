package com.example.projectname;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication
@EntityScan("com.example.projectname.*") // Ensures entities are scanned
@ComponentScan(basePackages = { "com.example.projectname.*" })
@EnableJpaRepositories("com.example.projectname.*") // Ensures repositories are scanned
public class ProjectnameApplication {

	public static void main(String[] args) {
		SpringApplication.run(ProjectnameApplication.class, args);
	}

}
