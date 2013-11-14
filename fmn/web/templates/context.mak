<%inherit file="master.mak"/>
<div class="jumbotron">
  <h1>${current.name} preferences</h1>
  <p>${current.description}</p>
</div>
<div class="row">
  <div class="md-col-6">
    <p>You have ${len(preference.chains)} filter chains
    defined for this messaging context.</p>
  </div>
</div>
<div class="row">
  <div class="md-col-6">
    <ul>
      % for chn in preference.chains:
      <li>${chn.name}</li>
      %endfor
    </ul>
  </div>
</div>
