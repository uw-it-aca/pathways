describe('home page', function() {

  context('accept modal', function() {

    // TODO: lower fidelity tests should match the workflow supported by the MVP
    // (e.g. test the button functionality)

    it('should display on initial launch', function() {
      cy.visit('/');
      // eslint-disable-next-line cypress/no-unnecessary-waiting
      cy.wait(500);
      cy.get('#home').should('exist');
      // take a snapshot
      cy.document().matchImageSnapshot();

    });

  });

});
